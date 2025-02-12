import pandas as pd
import os
from evolution_chains import get_evolution_chain
import matplotlib.pyplot as plt
from team_analyzer import TeamAnalyzer
import seaborn as sns

def calculate_stat_changes(base_pokemon, evolved_form):
    """Calculate stat differences between forms"""
    stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    return {
        stat: evolved_form[stat] - base_pokemon[stat]
        for stat in stats
    }

def analyze_evolution_option(current, evolved):
    """Analyze a single evolution option and return its characteristics"""
    stat_changes = calculate_stat_changes(current, evolved)
    total_change = sum(stat_changes.values())
    
    benefits = []
    drawbacks = []
    
    # Analyze offensive capabilities
    offensive_change = stat_changes['attack'] + stat_changes['sp_attack']
    if offensive_change > 30:
        benefits.append(f"Strong offensive improvement (+{offensive_change} total attack)")
    elif offensive_change < 0:
        drawbacks.append(f"Decreased offensive capability ({offensive_change} total attack)")
    
    # Analyze defensive capabilities
    defensive_change = stat_changes['defense'] + stat_changes['sp_defense'] + stat_changes['hp']
    if defensive_change > 45:
        benefits.append(f"Major defensive boost (+{defensive_change} total bulk)")
    elif defensive_change > 20:
        benefits.append(f"Improved survivability (+{defensive_change} total bulk)")
    
    # Speed analysis
    if stat_changes['speed'] > 20:
        benefits.append(f"Significant speed boost (+{stat_changes['speed']})")
    elif stat_changes['speed'] > 0:
        benefits.append(f"Slight speed improvement (+{stat_changes['speed']})")
    elif stat_changes['speed'] < 0:
        drawbacks.append(f"Speed decrease ({stat_changes['speed']})")
    
    # Type advantage analysis
    if current['type1'] != evolved['type1'] or current['type2'] != evolved['type2']:
        old_types = f"{current['type1']}"
        new_types = f"{evolved['type1']}"
        if pd.notna(current['type2']): old_types += f"/{current['type2']}"
        if pd.notna(evolved['type2']): new_types += f"/{evolved['type2']}"
        benefits.append(f"Type change: {old_types} → {new_types}")
    
    return {
        'name': evolved['name'],
        'stat_changes': stat_changes,
        'total_change': total_change,
        'benefits': benefits,
        'drawbacks': drawbacks
    }

def create_evolution_graph(pokemon_data_list, stats):
    """Create a stacked bar graph showing stat differences across evolution forms"""
    plt.figure(figsize=(14, 8))
    
    # Get base stats and prepare data
    base_pokemon = pokemon_data_list[0]
    base_values = [base_pokemon[stat.lower()] for stat in stats]
    
    # Calculate differences for each evolution
    differences = []
    names = [base_pokemon['name']]
    types = [f"{base_pokemon['type1']}{f'/{base_pokemon['type2']}' if pd.notna(base_pokemon['type2']) else ''}"]
    
    for evolved in pokemon_data_list[1:]:
        diff = [max(0, evolved[stat.lower()] - base_pokemon[stat.lower()]) for stat in stats]
        differences.append(diff)
        names.append(evolved['name'])
        types.append(f"{evolved['type1']}{f'/{evolved['type2']}' if pd.notna(evolved['type2']) else ''}")
    
    # Plot base stats
    x = range(len(stats))
    bars = plt.bar(x, base_values, label=base_pokemon['name'], color='#FF9999')
    
    # Add value labels for base stats
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    # Plot stat increases for each evolution
    bottom = base_values
    colors = ['#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
    
    for i, diff in enumerate(differences):
        bars = plt.bar(x, diff, bottom=bottom, label=f"{names[i+1]}", 
                      color=colors[i % len(colors)], alpha=0.7)
        
        # Add value labels for total stats
        for j, bar in enumerate(bars):
            total_height = bottom[j] + bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., total_height,
                    f'{int(total_height)}',
                    ha='center', va='bottom')
        
        bottom = [sum(x) for x in zip(bottom, diff)]
    
    # Customize the graph
    plt.xlabel('Stats')
    plt.ylabel('Value')
    plt.title(f'Evolution Chain Stats: {" → ".join(names)}')
    
    # Set x-axis labels (stats)
    plt.xticks(x, stats)
    
    # Add type information at the bottom
    type_text = '\n'.join([f"{name}: {type_}" for name, type_ in zip(names, types)])
    plt.figtext(0.99, 0.01, type_text, 
                horizontalalignment='right', 
                verticalalignment='bottom',
                fontsize=9,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Add grid and legend
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the graph
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(os.path.join(script_dir, 'evolution_stats.png'), 
                bbox_inches='tight', dpi=300)
    plt.close()

def get_full_evolution_chain(pokemon_name, df):
    """Get all Pokemon data in the evolution chain"""
    chain = get_evolution_chain(pokemon_name)
    if not chain:
        return [df[df['name'].str.upper() == pokemon_name.upper()].iloc[0]]
    
    pokemon_data_list = []
    current_chain = chain
    
    # Handle branching evolutions
    for stage in chain:
        if isinstance(stage, list):
            # For branching evolutions, we'll create separate chains
            # For now, let's just take the first branch for visualization
            stage = stage[0]
        pokemon_data = df[df['name'].str.upper() == stage].iloc[0]
        pokemon_data_list.append(pokemon_data)
    
    return pokemon_data_list

def analyze_evolution_options(pokemon_name, df):
    """Analyze all possible evolution options and provide recommendations"""
    chain = get_evolution_chain(pokemon_name)
    if not chain:
        return "No evolution data available."
    
    current = df[df['name'].str.upper() == pokemon_name.upper()].iloc[0]
    next_stage = chain[1] if len(chain) > 1 else None
    
    if not next_stage:
        return f"{pokemon_name} is fully evolved."
    
    output = [f"\nEvolution Analysis for {pokemon_name}"]
    output.append("=" * 50)
    
    # Get full evolution chain for visualization
    pokemon_data_list = get_full_evolution_chain(pokemon_name, df)
    
    # Create visualization with full chain
    stats = ['HP', 'Attack', 'Defense', 'Sp_Attack', 'Sp_Defense', 'Speed']
    create_evolution_graph(pokemon_data_list, stats)
    output.append("\nStat visualization has been saved as 'evolution_stats.png'")
    
    # Analyze immediate evolution options
    options = []
    if isinstance(next_stage, list):
        for evo_name in next_stage:
            evolved = df[df['name'].str.upper() == evo_name].iloc[0]
            options.append(analyze_evolution_option(current, evolved))
    else:
        evolved = df[df['name'].str.upper() == next_stage].iloc[0]
        options.append(analyze_evolution_option(current, evolved))
    
    # Sort options by total stat change
    options.sort(key=lambda x: x['total_change'], reverse=True)
    
    # Present each option with its analysis
    for i, option in enumerate(options, 1):
        output.append(f"\nOption {i}: {option['name']}")
        output.append("-" * 40)
        
        # Show stat changes
        output.append("Stat Changes:")
        for stat, change in option['stat_changes'].items():
            output.append(f"  {stat.upper()}: {'+' if change > 0 else ''}{change}")
        output.append(f"Total Stat Change: {'+' if option['total_change'] > 0 else ''}{option['total_change']}")
        
        # Show benefits and drawbacks
        if option['benefits']:
            output.append("\nBenefits:")
            for benefit in option['benefits']:
                output.append(f"✓ {benefit}")
        if option['drawbacks']:
            output.append("\nDrawbacks:")
            for drawback in option['drawbacks']:
                output.append(f"⚠ {drawback}")
    
    # Strategic recommendations
    output.append("\nStrategic Recommendations:")
    if len(options) > 1:
        output.append("Based on your battle strategy, consider:")
        for option in options:
            output.append(f"\n{option['name']}:")
            if option['benefits']:
                output.append(f"- Best for: {', '.join(b.split(':')[0] for b in option['benefits'])}")
    else:
        option = options[0]
        if not option['drawbacks']:
            output.append("✓ Recommended to evolve - clear improvements across stats")
        elif option['total_change'] > 40:
            output.append("○ Consider evolving - good improvements despite some drawbacks")
        else:
            output.append("⚠ Carefully consider evolution - mixed changes in stats")
    
    return "\n".join(output)

def analyze_team(df: pd.DataFrame) -> None:
    """Team analysis interface"""
    analyzer = TeamAnalyzer(df)
    
    print("\n🎮 Pokemon Team Analyzer")
    team = input("Enter your team of 6 Pokemon (comma-separated):\n").strip().split(',')
    team = [p.strip() for p in team]
    
    if len(team) != 6:
        print("⚠️ Please enter exactly 6 Pokemon!")
        return
    
    try:
        analysis = analyzer.analyze_team(team)
        analyzer.visualize_team_coverage(team)
        
        print("\n📊 Team Analysis Report")
        
        # Duplicates
        if analysis['balance']['duplicates']:
            print("\n⚠️ Duplicate Pokemon:")
            for name, count in analysis['balance']['duplicates'].items():
                print(f"- {name} (x{count})")
        
        # Coverage
        print("\n🛡️ Defensive Coverage:")
        print(f"Weaknesses: {', '.join(analysis['defense']['weaknesses'])}")
        print(f"Resistances: {', '.join(analysis['defense']['resistances'])}")
        
        print("\n⚔️ Offensive Coverage:")
        print(f"Types: {', '.join(analysis['offense'])}")
        
        # Stats
        print("\n📈 Team Stats (Average):")
        for stat, values in analysis['balance']['stats'].items():
            print(f"{stat.upper()}: {values['avg']:.1f} (Range: {values['min']}-{values['max']})")
        
        # Suggestions
        if analysis['suggestions']:
            print("\n💡 Improvement Suggestions:")
            
            for suggestion in analysis['suggestions']:
                if suggestion['type'] == 'duplicate':
                    print(f"\nReplace extra {suggestion['pokemon']} with:")
                    for replacement in suggestion['replacements']:
                        print(f"- {replacement['name']} ({replacement['types']}) - "
                              f"Base Total: {replacement['base_total']} - "
                              f"{replacement['evolution_stage']}"
                              f"{' (Can evolve!)' if replacement['can_evolve'] else ''}")
                
                elif suggestion['type'] == 'weakness':
                    print(f"\nTo cover {suggestion['weakness']} weakness, consider:")
                    for counter in suggestion['counters']:
                        print(f"- {counter['name']} ({counter['types']}) - "
                              f"Base Total: {counter['base_total']} - "
                              f"{counter['evolution_stage']}"
                              f"{' (Can evolve!)' if counter['can_evolve'] else ''}")
        
        print("\n📊 Team coverage chart saved as 'team_coverage.png'")
        
    except IndexError:
        print("❌ Error: One or more Pokemon not found in database")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

def show_menu():
    """Display interactive menu options"""
    print("\n🔍 Pokemon Evolution Advisor")
    print("1. Analyze specific Pokemon")
    print("2. Show dataset overview")
    print("3. Compare multiple Pokemon")
    print("4. Analyze team composition")
    print("5. Exit")

def main():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, 'pokemon.csv')
        df = pd.read_csv(csv_path)
        
        if 'total_stats' not in df.columns:
            df['total_stats'] = df[['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].sum(axis=1)
        
        while True:
            show_menu()
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1':
                pokemon_name = input("\nEnter Pokemon name: ").strip().lower()
                if pokemon_name == 'quit':
                    break
                print(analyze_evolution_options(pokemon_name, df))
                
            elif choice == '2':
                display_dataset_overview(df)
                
            elif choice == '3':
                pokemon_list = input("\nEnter Pokemon names (comma-separated): ").strip()
                pokemon_names = [name.strip() for name in pokemon_list.split(',')]
                
                print("\n🔄 Comparing Pokemon:")
                for name in pokemon_names:
                    pokemon_data = df[df['name'].str.lower() == name.lower()]
                    if len(pokemon_data) == 0:
                        print(f"\n❌ Pokemon '{name}' not found!")
                        continue
                    
                    pokemon = pokemon_data.iloc[0]
                    print(f"\n📊 {pokemon['name']}:")
                    print(f"Types: {pokemon['type1']}" + 
                          (f"/{pokemon['type2']}" if pd.notna(pokemon['type2']) else ""))
                    print(f"HP: {pokemon['hp']}")
                    print(f"Attack: {pokemon['attack']}")
                    print(f"Defense: {pokemon['defense']}")
                    print(f"Sp. Attack: {pokemon['sp_attack']}")
                    print(f"Sp. Defense: {pokemon['sp_defense']}")
                    print(f"Speed: {pokemon['speed']}")
                    print(f"Total: {pokemon['total_stats']}")
                
            elif choice == '4':
                analyze_team(df)
                
            elif choice == '5':
                print("\nThanks for using the Pokemon Evolution Advisor!")
                break
                
            else:
                print("\n❌ Invalid choice. Please select 1-5.")
            
    except FileNotFoundError:
        print(f"Error: Pokemon database file not found at {csv_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def display_dataset_overview(df):
    """Display basic information about the dataset"""
    print("\n📝 Dataset Overview:")
    print(f"Total number of Pokemon: {len(df)}")
    print(f"Number of generations: {df['generation'].nunique()}")
    print(f"Number of unique types: {df['type1'].nunique()}")
    
    print("\n📊 Statistical Summary of Base Stats:")
    stats_cols = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'total_stats']
    stats_summary = df[stats_cols].describe()
    
    # Format and display stats summary
    for stat in stats_cols:
        print(f"\n{stat.upper()}:")
        print(f"  Average: {stats_summary.loc['mean', stat]:.1f}")
        print(f"  Minimum: {stats_summary.loc['min', stat]:.0f}")
        print(f"  Maximum: {stats_summary.loc['max', stat]:.0f}")
    
    print("\n🔝 Top 5 Pokemon by total stats:")
    top_pokemon = df.nlargest(5, 'total_stats')[['name', 'type1', 'type2', 'total_stats']]
    for _, pokemon in top_pokemon.iterrows():
        types = f"{pokemon['type1']}" + (f"/{pokemon['type2']}" if pd.notna(pokemon['type2']) else "")
        print(f"  {pokemon['name']} ({types}): {pokemon['total_stats']:.0f}")

if __name__ == "__main__":
    main()
