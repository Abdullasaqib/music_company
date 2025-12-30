import random

class RiffusionAPI:
    def generate_spectrogram(self, prompt):
        # Simulation of Riffusion's Stable Diffusion interactions
        print(f"[Riffusion] Diffusion steps for prompt: '{prompt}'...")
        
        textures = ["Lo-fi Grain", "Synthwave Neon", "Ambient Wash", "8-bit Crunch"]
        
        return {
            "model": "Riffusion v1.5",
            "spectrogram_seed": random.randint(1000, 9999),
            "texture": random.choice(textures),
            "loop_perfect": True,
            "generation_time": round(random.uniform(2.0, 8.0), 2)
        }
