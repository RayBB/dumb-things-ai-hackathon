import os
import replicate
from replicate.exceptions import ReplicateException

tech_bro_quotes = {
    # "fish": [
    #     {"text": "The bay's getting cleaner, but the mercury levels in those bigger fish? Scary.", "audio_src": "voices/fish_1.wav"},
    #     {"text": "Can fish actually live in the bay?", "audio_src": "voices/fish_2.wav"},
    # ],
    # "pelican": [
    #     {"text": "These birds divebomb like Silicon Valley jumping on trends - total commitment.", "audio_src": "voices/pelican_1.wav"},
    #     {"text": "Pelican watching: nature's way of telling you to slow down for once."}
    # ],
    # "muni": [
    #     {"text": "Why am I always the one who gets stuck waiting while every other line runs perfect?"},
    #     {"text": "Waited 45 minutes for the 22 Fillmore again. Might as well walk to Oakland at this point."},
    # ],
    # "waymo": [
    #     {"text": "Waymos are stuck and are honking at each other during the night in San Francisco.", "audio_src": "voices/waymo_1.wav"},
    #     {"text": "Lets just take a Waymo. My last Uber driver talked too much.", "audio_src": "voices/waymo_2.wav"},
    # ],
    # "sealion": [
    #     {"text": "Barking at tourists since 1990. World's most patient tour guides.", "audio_src": "voices/sealion_1.wav"},
    #     {"text": "These sea lions have been holed up at Pier 39 for years - kinda our mascot now.", "audio_src": "voices/sealion_2.wav"},
    # ],
    # "fog": [
    #     {"text": "Fog's like the nice aunt who visits unannounced and wrecks your hair plans.", "audio_src": "voices/fog_1.wav"},
    #     {"text": "Karl the Fog strikes again - this bastard loves ruining perfectly good sunsets.", "audio_src": "voices/fog_2.wav"},
    #     {"text": "Fog's the one thing in SF that actually respects 'taking it slow'."}
    # ],
    "sourdough": [
        {"text": "Sourdough is SF's gold - better than rush, but don't get carried away by prospectors."},
        {"text": "Tartine bread line is longer than the N Judah wait during a delay."},
        {"text": "Sourdough's the only thing that rises reliably in this city besides housing costs."},
        {"text": "My sourdough starter outlasted my last startup and two relationships."}
    ],
    "cablecar": [
        {"text": "Tourists think it's cute. Locals think it's a daily lottery with physics."},
        {"text": "Cable car broke down again? Walk down Nob Hill - good cardio and same ETA."},
        {"text": "SF built these before were escalators. Shows what real innovation looked like."},
    ],
    # "ai_billboard": [
    #     {"text": "Billboards are a window into the soul of a city."},
    #     {"text": "Why does every billboard have to be an AI billboard?"},
    # ],
    # "transamerica": [
    #     {"text": "That pyramid's been the city's exclamation mark since I was knee-high to a fog bank."},
    #     {"text": "Height limit violator, architectural rebel. We love it for that."}
    # ],
    # "lacroix": [
    #     {"text": "Dude, all the Pamplemousse ran out? This is a supply chain FAILURE!"},
    #     {"text": "La Croix? I optimized my hydration with electrolyte-infused smart water instead."},
    #     {"text": "La Croix? Basic. I craft my own kombucha from biodynamic grapes in Napa."},
    #     {"text": "I invested in the startup making premium sparkling water pods last week."},
    # ],
    # "goldengate": [
    #     {"text": "Crossing the bridge always feels like entering another world - especially in the fog."},
    #     {"text": "That bridge has stared down earthquakes, fog, and millions of tourist selfies."},
    #     {"text": "Golden Gate at sunset? Pure magic. Worth every penny of toll."},
    #     {"text": "They painted it orange so ships can see it through the fog. Smart thinking."},
    #     {"text": "Half the reason I moved here was to jog across that bridge at dawn."},
    #     {"text": "Bridge closes for high winds? Perfect excuse to re-read my stack of library books."}
    # ],
    # "clipper": [
    #     {"text": "Getting seasick on the Larkspur? At least you're not on the 101 in rush hour."},
    #     {"text": "Ferry terminal dog: better commute accessory than any coworking space."},
    #     {"text": "Clipper card lost again? Third one this year. Dating myself with public transit woes."},
    #     {"text": "Sausalito ferry at dusk - unbeatable commute if you time the tides right."},
    #     {"text": "Golden Gate Ferry: because sometimes you need a break from the city's chaos."}
    # ],
    # "coyote": [
    #     {"text": "Coyote wandering up Delores at 3 AM. Welcome to SF living."},
    #     {"text": "Coyotes searching through my compost bin at midnight. Sustainable living has consequences."},
    #     {"text": "Coyotes in the backyard? Urban nature red in tooth and claw."}
    # ],
    # "ia": [
    #     {"text": "The internet archive preserves knowledge for future generations with open access."},
    #     {"text": "Timeless wisdom and human history safeguarded in digital eternity."},
    #     {"text": "Democratizing information through free archival preservation efforts."},
    #     {"text": "Bridging the past and future through dedicated knowledge stewardship."}
    # ],
    # "avocado": [
    #     {"text": "Avocado toast for $15? It's actually not a bad deal for this city."},
    #     {"text": "Avocados lack blockchain supply chain verification for fair trade credibility."},
    # ],
}

# Initialize Replicate client
replicate_client = replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"))

async def generate_audio_with_prompt(prompt, file_path):
    input_params = {
        "seed": 0,
        "prompt": prompt,
        "cfg_weight": 0.5,
        "temperature": 0.8,
        "exaggeration": 0.5
    }
    print(input_params)
    print("Generating audio for", file_path)
    try:
        output = await replicate_client.async_run("resemble-ai/chatterbox", input=input_params)
        # Assuming output is a file URL, need to fetch it
        # But in JS it's treated as data, so perhaps the model returns data directly
        # Replicate run typically returns URLs, so we may need to download
        # if isinstance(output, list) and output:
        audio_url = output
        import requests
        with requests.get(audio_url) as resp:
            audio_data = resp.content
            with open(file_path, "wb") as f:
                f.write(audio_data)
            import time
            time.sleep(10)
        # else:
        #     print(f"Unexpected output format: {output}")
    except ReplicateException as e:
        print(f"Error generating audio for {file_path}: {e}")

async def log_quotes_without_audio():
    for category, quotes in tech_bro_quotes.items():
        for index, quote in enumerate(quotes):
            if "audio_src" not in quote:
                file_path = f"voices/{category}_{index + 1}.wav"
                if not os.path.exists(file_path):
                    print(f'Quote: "{quote["text"]}"')
                    print(f"Appropriate file path: {file_path}")
                    await generate_audio_with_prompt(quote["text"], file_path)

if __name__ == "__main__":
    import asyncio
    asyncio.run(log_quotes_without_audio())
