import pandas as pd
import numpy as np
from typing import List, Dict
import matplotlib.pyplot as plt
import json
import os

class TeamAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.type_columns = [col for col in df.columns if col.startswith('against_')]
        self.stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        
        # Load evolution chains
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, 'evolution_chains.json')
        try:
            with open(json_path, 'r') as f:
                self.evolution_chains = json.load(f)
        except FileNotFoundError:
            print("Warning: evolution_chains.json not found. Generating new evolution chains...")
            from generate_evolution_chains import save_evolution_chains
            save_evolution_chains()
            with open(json_path, 'r') as f:
                self.evolution_chains = json.load(f)
    
    def get_pokemon_data(self, name: str) -> pd.Series:
        return self.df[self.df['name'].str.lower() == name.lower()].iloc[0]
    
    def analyze_team(self, team: List[str]) -> Dict:
        """Comprehensive team analysis"""
        team_data = [self.get_pokemon_data(name) for name in team]
        avg_base_total = sum(p['base_total'] for p in team_data) / len(team_data)
        
        return {
            'defense': self._analyze_defense(team_data),
            'offense': self._analyze_offense(team_data),
            'balance': self._analyze_balance(team_data),
            'suggestions': self._get_suggestions(team, team_data, avg_base_total)
        }
    
    def _analyze_defense(self, team_data: List[pd.Series]) -> Dict:
        """Analyze defensive coverage"""
        effectiveness = {
            col.replace('against_', ''): min(pokemon[col] for pokemon in team_data)
            for col in self.type_columns
        }
        return {
            'weaknesses': [t for t, e in effectiveness.items() if e > 1],
            'resistances': [t for t, e in effectiveness.items() if e < 1],
            'effectiveness': effectiveness
        }
    
    def _analyze_offense(self, team_data: List[pd.Series]) -> List[str]:
        """Analyze offensive coverage"""
        types = set()
        for pokemon in team_data:
            types.add(pokemon['type1'].lower())
            if pd.notna(pokemon['type2']):
                types.add(pokemon['type2'].lower())
        return list(types)
    
    def _analyze_balance(self, team_data: List[pd.Series]) -> Dict:
        """Analyze team balance"""
        # Check duplicates
        names = [p['name'] for p in team_data]
        duplicates = {name: names.count(name) for name in set(names) if names.count(name) > 1}
        
        # Analyze stats
        stat_analysis = {
            stat: {
                'avg': sum(p[stat] for p in team_data) / len(team_data),
                'min': min(p[stat] for p in team_data),
                'max': max(p[stat] for p in team_data)
            }
            for stat in self.stats
        }
        
        return {'duplicates': duplicates, 'stats': stat_analysis}
    
    def _get_suggestions(self, team: List[str], team_data: List[pd.Series], 
                        avg_base_total: float) -> List[Dict]:
        """Get team improvement suggestions"""
        stat_range = avg_base_total * 0.20
        suggestions = []
        
        # Handle duplicates
        for name, count in self._analyze_balance(team_data)['duplicates'].items():
            replacements = self.df[
                (self.df['base_total'].between(avg_base_total - stat_range, avg_base_total + stat_range)) &
                (self.df['type1'] != self.get_pokemon_data(name)['type1']) &
                (~self.df['name'].isin(team)) &
                (~self.df['is_legendary'])
            ].nlargest(3, 'base_total')
            
            suggestions.append({
                'type': 'duplicate',
                'pokemon': name,
                'count': count,
                'replacements': [self._format_pokemon(p) for _, p in replacements.iterrows()]
            })
        
        # Handle weaknesses
        defense = self._analyze_defense(team_data)
        for weakness in defense['weaknesses']:
            counters = self.df[
                (self.df[f'against_{weakness}'] < 1) &
                (self.df['base_total'].between(avg_base_total - stat_range, avg_base_total + stat_range)) &
                (~self.df['name'].isin(team)) &
                (~self.df['is_legendary'])
            ].nlargest(3, 'base_total')
            
            if not counters.empty:
                suggestions.append({
                    'type': 'weakness',
                    'weakness': weakness,
                    'counters': [self._format_pokemon(p) for _, p in counters.iterrows()]
                })
        
        return suggestions
    
    def get_evolution_info(self, pokemon_name: str) -> Dict:
        """Get evolution information for a Pokemon"""
        name_upper = pokemon_name.upper()
        chain = self.evolution_chains.get(name_upper, [])
        
        if not chain:
            return {
                'stage': 0,
                'total_stages': 0,
                'can_evolve': False
            }
        
        if isinstance(chain[-1], list):  # Handle branching evolutions
            current_stage = chain.index(name_upper) + 1 if name_upper in chain else 1
            total_stages = len(chain)
        else:
            current_stage = chain.index(name_upper) + 1
            total_stages = len(chain)
        
        return {
            'stage': current_stage,
            'total_stages': total_stages,
            'can_evolve': current_stage < total_stages
        }
    
    def _format_pokemon(self, pokemon: pd.Series) -> Dict:
        """Format Pokemon data for output, including evolution info"""
        evo_info = self.get_evolution_info(pokemon['name'])
        
        return {
            'name': pokemon['name'],
            'types': f"{pokemon['type1']}" + (f"/{pokemon['type2']}" if pd.notna(pokemon['type2']) else ""),
            'base_total': pokemon['base_total'],
            'evolution_stage': f"Stage {evo_info['stage']}/{evo_info['total_stages']}" 
                             if evo_info['total_stages'] > 0 
                             else "Final Form",
            'can_evolve': evo_info['can_evolve']
        }
    
    def visualize_team_coverage(self, team: List[str]) -> None:
        """Create radar chart of team's defensive coverage"""
        defense = self._analyze_defense([self.get_pokemon_data(name) for name in team])
        types = sorted(defense['effectiveness'].keys())
        
        angles = np.linspace(0, 2*np.pi, len(types), endpoint=False)
        values = [defense['effectiveness'][t] for t in types]
        
        values.append(values[0])
        angles = np.append(angles, angles[0])
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(types)
        ax.set_title("Team Type Coverage")
        ax.set_rticks([0.5, 1, 2])
        ax.set_rlabel_position(0)
        ax.grid(True)
        
        plt.savefig('team_coverage.png')
        plt.close() 