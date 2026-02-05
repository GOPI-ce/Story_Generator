"""
Scene Generator - Creates actual story content with dialogue
Uses prompt chaining for consistent character voices
Built by: [Your Name]
"""

import json
from typing import Dict, List
import os
from datetime import datetime

# Try to import OpenAI for OpenRouter, fall back to mock if not available
try:
    from openai import OpenAI
    api_key = os.getenv('GEMINI_API_KEY')  # Using same env var name
    if api_key:
        # Configure OpenRouter client
        openrouter_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        OPENROUTER_MODEL = "google/gemini-3-flash-preview"
        HAS_OPENROUTER = True
        print("[DONE] OpenRouter configured successfully")
        print(f"   Model: {OPENROUTER_MODEL}")
    else:
        HAS_OPENROUTER = False
        print("[WARN] GEMINI_API_KEY not set - will use mock generation for demo")
except Exception as e:
    HAS_OPENROUTER = False
    print(f"[WARN] OpenRouter not available ({e}) - will use mock generation for demo")

class SceneGenerator:
    """
    Generates story scenes with dialogue using structured prompts
    Key innovation: Character voice consistency through trait injection
    """
    
    def __init__(self, story_data_file: str):
        with open(story_data_file, 'r', encoding='utf-8') as f:
            self.story = json.load(f)
        
        # Extract character voice profiles
        self.voice_profiles = self._create_voice_profiles()
        
        print(f"[THEATER] Loaded story: {self.story['title']}")
        print(f"   Characters: {len(self.voice_profiles)}")
    
    def _create_voice_profiles(self) -> Dict:
        """Create consistent voice profiles for each character"""
        profiles = {}
        
        for char in self.story['transformed_characters']:
            name = char['name']
            profiles[name] = {
                'core_traits': char['core_traits'],
                'speaking_style': self._infer_speaking_style(char),
                'vocabulary': self._infer_vocabulary(char),
                'sentence_patterns': self._infer_patterns(char)
            }
        
        return profiles
    
    def _infer_speaking_style(self, char: Dict) -> str:
        """Infer how character speaks from traits"""
        traits = char['core_traits']
        
        if 'obsessive' in str(traits).lower() or 'arrogant' in str(traits).lower():
            return "Precise, rapid-fire, uses technical jargon, interrupts others"
        elif 'grounded' in str(traits).lower():
            return "Measured, explanatory, translates complex ideas simply"
        elif 'brilliant' in str(traits).lower():
            return "Cryptic, confident, speaks in puzzles and hints"
        elif 'desperate' in str(traits).lower():
            return "Nervous, pleading, fragmented sentences when stressed"
        else:
            return "Professional, straightforward"
    
    def _infer_vocabulary(self, char: Dict) -> List[str]:
        """Words this character would use"""
        profession = char.get('profession', '').lower()
        
        if 'consultant' in profession or 'data' in profession:
            return ["patterns", "anomalies", "correlation", "encryption", "algorithms"]
        elif 'chronicler' in profession or 'engineer' in profession:
            return ["document", "observe", "explain", "understand", "human"]
        elif 'security' in profession or 'researcher' in profession:
            return ["breach", "trace", "shadow", "ghost", "unseen"]
        else:
            return ["sir", "please", "help", "problem", "solution"]
    
    def _infer_patterns(self, char: Dict) -> List[str]:
        """Sentence structures this character uses"""
        name = char['name']
        
        patterns = {
            'Surya': [
                "The data suggests...",
                "Elementary pattern recognition.",
                "You're missing the correlation between..."
            ],
            'Gopi': [
                "I should explain...",
                "From my perspective...",
                "What Surya means is..."
            ],
            'Venkat': [
                "You assume...",
                "Predictable.",
                "Three steps ahead, as always."
            ],
            'Bhuvan': [
                "Please, you must...",
                "I don't understand...",
                "My career depends on this!"
            ]
        }
        
        return patterns.get(name, ["", "", ""])
    
    def generate_scene(self, scene_number: int) -> str:
        """Generate a complete scene with dialogue"""
        beat = self.story['transformed_plot'][scene_number - 1]
        
        print(f"\n[MOVIE] Generating Scene {scene_number}: {beat['title']}")
        
        # Build context for this scene
        context = {
            'scene_title': beat['title'],
            'setting': beat.get('setting_details', {}),
            'emotional_tone': beat['emotional_tone'],
            'stakes': beat['cyberpunk_stakes'],
            'key_elements': beat.get('key_elements', [])
        }
        
        # Determine which characters appear
        characters_in_scene = self._identify_characters(beat['cyberpunk_event'])
        
        if HAS_OPENROUTER:
            return self._generate_with_openrouter(context, characters_in_scene)
        else:
            return self._generate_mock(context, characters_in_scene)
    
    def _identify_characters(self, event: str) -> List[str]:
        """Identify which characters appear in this event"""
        characters = []
        names = ['Surya', 'Gopi', 'Venkat', 'Bhuvan', 'Mahesh']
        
        for name in names:
            if name in event:
                characters.append(name)
        
        # Scene 1 always has client
        if not characters and 'arrives' in event.lower():
            characters = ['Surya', 'Bhuvan']
        
        return characters if characters else ['Surya', 'Gopi']
    
    def _generate_with_openrouter(self, context: Dict, characters: List[str]) -> str:
        """Generate scene using OpenRouter with structured prompting"""
        
        # Build character voice instructions
        voice_instructions = []
        for char in characters:
            profile = self.voice_profiles.get(char, {})
            voice_instructions.append(f"""
{char}:
- Speaking style: {profile.get('speaking_style', 'Normal')}
- Key vocabulary: {', '.join(profile.get('vocabulary', [])[:3])}
- Typical phrases: {' | '.join(profile.get('sentence_patterns', [])[:2])}
""")
        
        prompt = f"""You are an expert cyberpunk fiction writer. Write a scene from a cyberpunk mystery story set in Bangalore, 2089.

SCENE CONTEXT:
- Title: {context['scene_title']}
- Setting: {context['setting']}
- Emotional tone: {context['emotional_tone']}
- Stakes: {context['stakes']}
- Must include: {', '.join(context['key_elements'])}

CHARACTER VOICES (CRITICAL - maintain these consistently):
{chr(10).join(voice_instructions)}

REQUIREMENTS:
1. 800-1000 words
2. Include dialogue for all characters listed
3. Maintain distinct voices for each character (use their vocabulary!)
4. Include sensory details about Bangalore setting (Electronic City, neon, filter coffee, etc.)
5. Show, don't tell - reveal character through actions and speech
6. End with a hook or revelation

Write the scene now:"""

        try:
            response = openrouter_client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert cyberpunk fiction writer. You excel at maintaining distinct character voices and creating atmospheric scenes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[WARN] OpenRouter error: {e}")
            return self._generate_mock(context, characters)
    
    def _generate_mock(self, context: Dict, characters: List[str]) -> str:
        """Generate mock scene when LLM unavailable"""
        scene_title = context['scene_title']
        
        lines = [f"# {scene_title}", ""]
        lines.append(f"*Setting: {context['setting'].get('location', 'Electronic City, Bangalore')}*")
        lines.append(f"*Atmosphere: {context['emotional_tone']}*")
        lines.append("")
        
        # Add dialogue based on characters
        if 'Bhuvan' in characters:
            lines.append(f"**Bhuvan:** (voice trembling) \"Please, you have to help me. My entire career--15 years at NexusCorp--it's all about to collapse.\"")
            lines.append("")
        
        if 'Surya' in characters:
            lines.append(f"**Surya:** (not looking up from data streams) \"Another corporate drone with a self-inflicted problem. How... mundane.\"")
            lines.append("")
            lines.append("*He swirls filter coffee, watching the steam rise in the neon glow of Electronic City*")
            lines.append("")
        
        if 'Gopi' in characters:
            lines.append(f"**Gopi:** \"What Surya means is, we're listening. Why don't you start from the beginning?\"")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append(f"*[MOCK SCENE - Enable Gemini for full generation]*")
        lines.append(f"*Key elements to include: {', '.join(context['key_elements'])}*")
        lines.append(f"*Stakes: {context['stakes']}*")
        
        return '\n'.join(lines)
    
    def generate_full_story(self) -> str:
        """Generate all scenes"""
        print("\n" + "="*60)
        print("GENERATING FULL STORY WITH DIALOGUE")
        print("="*60)
        
        all_scenes = []
        
        for i in range(len(self.story['transformed_plot'])):
            scene = self.generate_scene(i + 1)
            all_scenes.append(scene)
            
            # Add separator
            if i < len(self.story['transformed_plot']) - 1:
                all_scenes.append("\n\n" + "="*60 + "\n\n")
        
        return '\n'.join(all_scenes)


def main():
    """Generate complete story"""
    print("="*60)
    print("[MOVIE] SCENE GENERATOR")
    print("Creating dialogue and narrative")
    print("="*60)
    
    # Initialize
    generator = SceneGenerator("transformed_story.json")
    
    # Generate story
    full_story = generator.generate_full_story()
    
    # Save
    with open("complete_story.md", 'w', encoding='utf-8') as f:
        f.write(full_story)
    
    print(f"\n[SAVE] Complete story saved to: complete_story.md")
    print(f"   Scenes generated: {len(generator.story['transformed_plot'])}")
    
    if not HAS_OPENROUTER:
        print("\n[WARN] NOTE: Running in DEMO mode (no OpenRouter)")
        print("   Set GEMINI_API_KEY environment variable for full generation")
    
    return full_story


if __name__ == "__main__":
    story = main()
