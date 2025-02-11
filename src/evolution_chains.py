"""
Pokemon evolution chains from generations 1-7.
Format: 'BASE_POKEMON': ['BASE_POKEMON', 'FIRST_EVOLUTION', 'FINAL_EVOLUTION']
"""
import json
import os

# Define special evolution chains that need manual specification
SPECIAL_CHAINS = {
    # Eevee and Eeveelutions
    'EEVEE': ['EEVEE', ['VAPOREON', 'JOLTEON', 'FLAREON', 'ESPEON', 'UMBREON', 'LEAFEON', 'GLACEON', 'SYLVEON']],
    'VAPOREON': ['VAPOREON'],
    'JOLTEON': ['JOLTEON'],
    'FLAREON': ['FLAREON'],
    'ESPEON': ['ESPEON'],
    'UMBREON': ['UMBREON'],
    'LEAFEON': ['LEAFEON'],
    'GLACEON': ['GLACEON'],
    'SYLVEON': ['SYLVEON'],
    
    # Tyrogue evolutions
    'TYROGUE': ['TYROGUE', ['HITMONLEE', 'HITMONCHAN', 'HITMONTOP']],
    'HITMONLEE': ['HITMONLEE'],
    'HITMONCHAN': ['HITMONCHAN'],
    'HITMONTOP': ['HITMONTOP'],
    
    # Split evolutions
    'ODDISH': ['ODDISH', 'GLOOM', ['VILEPLUME', 'BELLOSSOM']],
    'GLOOM': ['GLOOM', ['VILEPLUME', 'BELLOSSOM']],
    'VILEPLUME': ['VILEPLUME'],
    'BELLOSSOM': ['BELLOSSOM'],
    
    'POLIWAG': ['POLIWAG', 'POLIWHIRL', ['POLIWRATH', 'POLITOED']],
    'POLIWHIRL': ['POLIWHIRL', ['POLIWRATH', 'POLITOED']],
    'POLIWRATH': ['POLIWRATH'],
    'POLITOED': ['POLITOED'],
    
    # Regular evolution chains
    'BULBASAUR': ['BULBASAUR', 'IVYSAUR', 'VENUSAUR'],
    'IVYSAUR': ['IVYSAUR', 'VENUSAUR'],
    'VENUSAUR': ['VENUSAUR'],
    
    'CHARMANDER': ['CHARMANDER', 'CHARMELEON', 'CHARIZARD'],
    'CHARMELEON': ['CHARMELEON', 'CHARIZARD'],
    'CHARIZARD': ['CHARIZARD'],
    
    'SQUIRTLE': ['SQUIRTLE', 'WARTORTLE', 'BLASTOISE'],
    'WARTORTLE': ['WARTORTLE', 'BLASTOISE'],
    'BLASTOISE': ['BLASTOISE'],
    
    # Add more evolution chains...
}

def load_evolution_chains():
    """Load evolution chains from JSON file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'evolution_chains.json')
    
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Evolution chains file not found. Generating new one...")
        from generate_evolution_chains import save_evolution_chains
        if save_evolution_chains():
            with open(json_path, 'r') as f:
                return json.load(f)
        return {}

EVOLUTION_CHAINS = load_evolution_chains()

def get_evolution_chain(pokemon_name):
    """
    Get the evolution chain for a given Pokemon.
    Args:
        pokemon_name (str): Name of the Pokemon (case insensitive)
    Returns:
        list: Evolution chain or None if not found
        For split evolutions, returns a list where the last element might be a list of options
    """
    pokemon_name = pokemon_name.upper()
    
    # Check special chains first
    if pokemon_name in SPECIAL_CHAINS:
        return SPECIAL_CHAINS[pokemon_name]
    
    # Search through all chains for the pokemon
    for chain in SPECIAL_CHAINS.values():
        if pokemon_name in chain:
            start_idx = chain.index(pokemon_name)
            return chain[start_idx:]
        # Check in split evolution options
        for item in chain:
            if isinstance(item, list) and pokemon_name in item:
                return [pokemon_name]
    
    return None

def get_next_evolution(pokemon_name):
    """
    Get the next evolution(s) for a given Pokemon.
    Returns a list if multiple evolution options exist.
    """
    chain = get_evolution_chain(pokemon_name)
    if not chain:
        return None
        
    if len(chain) > 1:
        next_evo = chain[1]
        if isinstance(next_evo, list):
            return next_evo  # Return all evolution options
        return next_evo
    return None

def get_final_evolution(pokemon_name):
    """
    Get the final evolution(s) for a given Pokemon.
    Returns a list if multiple final forms exist.
    """
    chain = get_evolution_chain(pokemon_name)
    if not chain:
        return None
        
    last_element = chain[-1]
    if isinstance(last_element, list):
        return last_element  # Return all final form options
    return last_element

def print_evolution_info(pokemon_name):
    """Print detailed evolution information for a Pokemon"""
    chain = get_evolution_chain(pokemon_name.upper())
    if not chain:
        print(f"{pokemon_name} has no evolution data available.")
        return
        
    print(f"\nEvolution chain for {pokemon_name}:")
    for i, element in enumerate(chain):
        if isinstance(element, list):
            print(f"Evolution options: {', '.join(element)}")
        else:
            print(f"Stage {i+1}: {element}") 