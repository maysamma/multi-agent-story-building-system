"""
Multi-Agent Creative Story Building System — Streamlit App
Agents: Story Planner · Character Designer · World Builder · Scene Writer
"""

import streamlit as st
import json
import random
import os
import time
from typing import Dict, List

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Story Builder",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');

/* ── Global ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1333 40%, #24243e 100%);
}

/* ── Hero header ────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    background: linear-gradient(135deg, #f5af19, #f12711, #c471ed, #12c2e9);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 6s ease infinite;
    margin-bottom: 0.2rem;
}
.hero p {
    color: #a0a0c0;
    font-size: 1.05rem;
    font-weight: 300;
    letter-spacing: 0.03em;
}
@keyframes gradient-shift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Agent cards ────────────────────────────────────── */
.agent-card {
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.agent-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}
.agent-card h3 {
    margin: 0 0 0.3rem;
    font-weight: 700;
    font-size: 1.1rem;
}
.agent-card p {
    margin: 0;
    font-size: 0.88rem;
    line-height: 1.5;
    color: #c0c0d8;
}

.card-planner   { background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(99,102,241,0.06)); }
.card-planner h3 { color: #818cf8; }
.card-character { background: linear-gradient(135deg, rgba(244,114,182,0.18), rgba(244,114,182,0.06)); }
.card-character h3 { color: #f472b6; }
.card-world     { background: linear-gradient(135deg, rgba(52,211,153,0.18), rgba(52,211,153,0.06)); }
.card-world h3  { color: #34d399; }
.card-scene     { background: linear-gradient(135deg, rgba(251,191,36,0.18), rgba(251,191,36,0.06)); }
.card-scene h3  { color: #fbbf24; }

/* ── Step progress ──────────────────────────────────── */
.step-badge {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 0.5rem;
}
.step-active   { background: rgba(99,102,241,0.25); color: #a5b4fc; border: 1px solid rgba(99,102,241,0.4); }
.step-done     { background: rgba(52,211,153,0.2);  color: #6ee7b7; border: 1px solid rgba(52,211,153,0.35); }

/* ── Output panels ──────────────────────────────────── */
.output-panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    color: #e0e0f0;
    font-size: 0.92rem;
    line-height: 1.7;
    white-space: pre-wrap;
}

/* ── Comm log ───────────────────────────────────────── */
.log-entry {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.45rem 0;
    font-size: 0.85rem;
    color: #b0b0cc;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.log-arrow { color: #818cf8; font-weight: 700; }

/* ── Buttons ────────────────────────────────────────── */
div.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.02em;
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #818cf8, #a78bfa);
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(99,102,241,0.35);
}

/* ── Sidebar ────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.95);
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* ── Input box ──────────────────────────────────────── */
.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #e0e0f0 !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.15) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ───────────────────────────────────────────────────────
if "interactions" not in st.session_state:
    st.session_state.interactions = []
if "results" not in st.session_state:
    st.session_state.results = {}
if "running" not in st.session_state:
    st.session_state.running = False

# ═════════════════════════════════════════════════════════════════════════════
# TOOLS
# ═════════════════════════════════════════════════════════════════════════════
from langchain_core.tools import tool

@tool
def genre_inspiration(genre: str) -> str:
    """Provide storytelling inspiration based on genre. Returns themes, tropes, and ideas."""
    inspirations = {
        "fantasy": {
            "themes": ["chosen one", "power corrupts", "nature vs. industry", "legacy of ancient magic"],
            "tropes": ["prophecy", "magic academy", "dark lord", "enchanted artifact", "quest"],
            "ideas": ["A spell that rewrites history every time it's cast", "A kingdom where dreams are currency"]
        },
        "sci-fi": {
            "themes": ["identity in technology", "ethics of AI", "colonization", "time paradox"],
            "tropes": ["generation ship", "rogue AI", "first contact", "cybernetic uprising"],
            "ideas": ["A planet where gravity shifts every 12 hours", "Humans who upload consciousness to escape a dying Earth"]
        },
        "mystery": {
            "themes": ["truth vs. deception", "justice vs. revenge", "hidden identity"],
            "tropes": ["locked room", "unreliable narrator", "cold case", "double cross"],
            "ideas": ["A detective investigating their own future murder", "A library where banned books reveal real crimes"]
        },
        "horror": {
            "themes": ["isolation", "the unknown", "loss of control", "doppelgangers"],
            "tropes": ["haunted house", "body horror", "cosmic dread", "cursed object"],
            "ideas": ["Mirrors that show a version of you that died", "A town where nobody can leave after dark"]
        },
        "cyberpunk": {
            "themes": ["surveillance state", "body augmentation", "class warfare", "digital identity"],
            "tropes": ["megacorp conspiracy", "hacker underworld", "memory manipulation", "neon noir"],
            "ideas": ["A black market for stolen memories", "An AI that develops genuine emotion and demands rights"]
        },
        "romance": {
            "themes": ["forbidden love", "second chances", "self-discovery through connection"],
            "tropes": ["enemies to lovers", "fake dating", "found family", "star-crossed"],
            "ideas": ["Two rival chefs fall in love through anonymous letters", "A time traveler who keeps meeting the same person in every era"]
        },
        "thriller": {
            "themes": ["paranoia", "survival", "conspiracy", "moral ambiguity"],
            "tropes": ["ticking clock", "double agent", "unreliable memory", "the heist"],
            "ideas": ["A whistleblower hunted by their own organization", "A hostage negotiator who realizes the hostage is the real threat"]
        },
    }
    genre_lower = genre.lower().strip()
    if genre_lower in inspirations:
        return json.dumps(inspirations[genre_lower], indent=2)
    return f"Genre '{genre}' not found. Available: {', '.join(inspirations.keys())}. General advice: Focus on conflict, stakes, and emotional resonance."


@tool
def character_name_generator(input_str: str) -> str:
    """Generate fitting character names based on culture. Provide input as a single string (e.g. 'western', 'eastern', 'arabic')."""
    culture = input_str.lower().strip()
    pools = {
        "western": ["Elara","Caden","Lyric","Thorne","Vesper","Rowan","Sage","Rhys","Wren","Darian"],
        "eastern": ["Kaito","Yuki","Haruki","Mei","Ren","Akira","Suki","Jin","Hana","Kael"],
        "arabic": ["Zara","Idris","Layla","Tariq","Nadia","Khalid","Amira","Farid","Soraya","Rami"],
        "latin": ["Lucian","Valentina","Marco","Isolde","Rafael","Celeste","Dante","Aria","Felix","Luna"],
        "nordic": ["Astrid","Bjorn","Freya","Leif","Sigrid","Torin","Eira","Ragnar","Sif","Alva"],
        "african": ["Amara","Kofi","Nia","Jabari","Zuri","Tendai","Imani","Oberon","Adaeze","Sekou"],
    }
    # Simple parsing logic to avoid validation errors
    valid_cultures = list(pools.keys())
    matched_culture = next((c for c in valid_cultures if c in culture), "western")

    pool = pools[matched_culture]
    selected = random.sample(pool, min(4, len(pool)))
    result = f"Suggested names ({matched_culture} culture):\n"
    for n in selected:
        result += f"  - {n}\n"
    return result


@tool
def plot_twist_generator(current_plot_summary: str) -> str:
    """Suggest unexpected plot twists based on the current plot summary."""
    twists = [
        "The mentor figure has been the true antagonist all along.",
        "The protagonist discovers they are a clone — the original is the villain.",
        "The 'safe haven' was destroyed long before they set out.",
        "A secondary character's hobby is the key to defeating the antagonist.",
        "The timeline is not linear — events happen simultaneously in different eras.",
        "The antagonist's motivation is genuinely noble, forcing the protagonist to question their side.",
        "A character believed dead has been secretly guiding events.",
        "The magical/technological system has a catastrophic flaw only the protagonist can trigger.",
        "The love interest is an undercover agent for the opposing faction.",
        "The entire quest was a test designed by a higher power.",
    ]
    selected = random.sample(twists, 3)
    result = f"Based on: '{current_plot_summary[:80]}...'\n\nSuggested twists:\n"
    for i, t in enumerate(selected, 1):
        result += f"  {i}. {t}\n"
    return result


# ═════════════════════════════════════════════════════════════════════════════
# AGENTS
# ═════════════════════════════════════════════════════════════════════════════
def build_agents(api_key: str):
    """Create all four agent executors."""
    os.environ["OPENAI_API_KEY"] = api_key

    from langchain_openai import ChatOpenAI
    from langchain.agents import create_react_agent, AgentExecutor
    from langsmith import Client

    client = Client()
    react_prompt = client.pull_prompt("hwchase17/react", dangerously_pull_public_prompt=True)

    balanced_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
    creative_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

    # ── Planner ──
    planner_instruction = """You are a Story Planner Agent.
Your ONLY job is to analyze the user's story idea and create a narrative structure.
Rules: Do NOT write full scenes. Focus ONLY on plot structure.
You may use genre_inspiration and plot_twist_generator tools.
Output: Genre & Tone, Act 1, Act 2, Act 3, Core Conflict, Key Themes."""

    planner_tools = [genre_inspiration, plot_twist_generator]
    planner_agent = create_react_agent(llm=balanced_llm, tools=planner_tools,
                                       prompt=react_prompt.partial(system_message=planner_instruction))
    planner_exec = AgentExecutor(agent=planner_agent, tools=planner_tools,
                                 verbose=False, max_iterations=10, handle_parsing_errors=True)

    # ── Character Designer ──
    character_instruction = """You are a Character Designer Agent.
Your ONLY job is to design memorable characters. Avoid clichés. Match genre.
Use character_name_generator for names.
For each character: Name, Role, Personality, Strengths, Flaws, Goals, Fears, Backstory, Relationships, Arc.
Create at least 3 characters."""

    char_tools = [character_name_generator]
    char_agent = create_react_agent(llm=balanced_llm, tools=char_tools,
                                    prompt=react_prompt.partial(system_message=character_instruction))
    char_exec = AgentExecutor(agent=char_agent, tools=char_tools,
                              verbose=False, max_iterations=10, handle_parsing_errors=True)

    from langchain.prompts import ChatPromptTemplate

    # ── World Builder ──
    world_instruction = """You are a World Builder Agent.
Your ONLY job is to create an immersive, internally consistent setting.
Output: Key Locations (3+), Society & Culture, Rules, Environment, Political Systems, Tech/Magic."""
    world_prompt = ChatPromptTemplate.from_messages([
        ("system", world_instruction),
        ("user", "{input}")
    ])
    world_exec = world_prompt | balanced_llm

    # ── Scene Writer ──
    scene_instruction = """You are a Scene Writer Agent.
Your ONLY job is to write compelling narrative scenes using the outline, characters, and world data.
Requirements: natural dialogue, emotional pacing, vivid descriptions, coherent transitions.
Rules: Do NOT change the plot. Do NOT invent new major characters. Do NOT contradict world rules.
CRITICAL: You MUST write the actual full story chapters in prose. Do NOT write a summary or overview. Write out the complete scenes with dialogue, action, and detailed descriptions. Give me the fully fleshed-out story text!
Output: The full text of the story chapters in detailed prose."""
    scene_prompt = ChatPromptTemplate.from_messages([
        ("system", scene_instruction),
        ("user", "{input}")
    ])
    scene_exec = scene_prompt | creative_llm

    return planner_exec, char_exec, world_exec, scene_exec


# ═════════════════════════════════════════════════════════════════════════════
# PIPELINE
# ═════════════════════════════════════════════════════════════════════════════
def run_pipeline(user_idea: str, planner_exec, char_exec, world_exec, scene_exec):
    """Run the 4-step multi-agent story pipeline with live UI updates."""

    st.session_state.interactions = []
    st.session_state.results = {}
    interactions = st.session_state.interactions
    results = st.session_state.results

    progress = st.progress(0, text="Initializing agents…")

    with st.status("Agents are collaborating on your story...", expanded=True) as status:
        # ── STEP 1 ─────────────────────────────────────────────────────────────
        st.write("🗺️ Story Planner is creating the narrative structure...")
        planner_input = f"""Create a detailed story outline for: \"{user_idea}\"
Use genre_inspiration for thematic ideas. Use plot_twist_generator for a twist.
Provide: Genre & Tone, Act 1, Act 2, Act 3, Core Conflict, Key Themes."""
        r = planner_exec.invoke({"input": planner_input})
        results["outline"] = r["output"]
        interactions.append({"from": "Planner", "to": "Character Designer", "msg": "Story outline ready"})
        progress.progress(25, text="Step 1 done — outline created")

        # ── STEP 2 ─────────────────────────────────────────────────────────────
        st.write("🎭 Character Designer is creating characters...")
        char_input = f"""Based on this outline, design the main characters:

STORY OUTLINE:
{results['outline']}

Create at least 3 characters. Use character_name_generator.
For each: Name, Role, Personality, Strengths, Flaws, Goals, Fears, Backstory, Relationships, Arc."""
        r = char_exec.invoke({"input": char_input})
        results["characters"] = r["output"]
        interactions.append({"from": "Character Designer", "to": "World Builder", "msg": "Characters designed"})
        progress.progress(50, text="Step 2 done — characters designed")

        # ── STEP 3 ─────────────────────────────────────────────────────────────
        st.write("🌍 World Builder is designing the setting...")
        world_input = f"""Build the world.

STORY OUTLINE:
{results['outline']}

CHARACTERS:
{results['characters']}

Create: Key Locations (3+), Society, Rules, Environment, Political Systems, Tech/Magic."""
        r = world_exec.invoke({"input": world_input})
        results["world"] = r.content
        interactions.append({"from": "World Builder", "to": "Scene Writer", "msg": "World constructed"})
        progress.progress(75, text="Step 3 done — world built")

        # ── STEP 4 ─────────────────────────────────────────────────────────────
        st.write("✍️ Scene Writer is writing the final story...")
        scene_input = f"""Write a compelling story.

STORY OUTLINE:
{results['outline']}

CHARACTERS:
{results['characters']}

WORLD:
{results['world']}

Write at least 2 chapters covering Acts 1–2. Include dialogue, vivid descriptions, emotional pacing.
Follow the outline — do not change the plot."""
        r = scene_exec.invoke({"input": scene_input})
        results["story"] = r.content
        interactions.append({"from": "Scene Writer", "to": "User", "msg": "Story delivered"})
        progress.progress(100, text="All steps complete ✨")
        
        status.update(label="Story Generation Complete!", state="complete", expanded=False)

    st.markdown("### ✨ Final Story")
    st.markdown(f'<div class="output-panel">{results["story"]}</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# UI LAYOUT
# ═════════════════════════════════════════════════════════════════════════════

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>📖 Multi-Agent Story Builder</h1>
    <p>Four AI agents collaborate to turn your idea into a rich, detailed story</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")

    st.markdown("---")
    st.markdown("## 🤖 Agent Team")

    st.markdown("""
    <div class="agent-card card-planner">
        <h3>🗺️ Story Planner</h3>
        <p>Analyzes your idea → genre, tone, 3-act structure, core conflict</p>
    </div>
    <div class="agent-card card-character">
        <h3>🎭 Character Designer</h3>
        <p>Creates protagonists, antagonists & supporting cast with depth</p>
    </div>
    <div class="agent-card card-world">
        <h3>🌍 World Builder</h3>
        <p>Designs locations, society, rules, technology & magic systems</p>
    </div>
    <div class="agent-card card-scene">
        <h3>✍️ Scene Writer</h3>
        <p>Writes vivid prose with dialogue, pacing & sensory detail</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Communication Log ──
    if st.session_state.interactions:
        st.markdown("---")
        st.markdown("## 📡 Agent Communication")
        for entry in st.session_state.interactions:
            st.markdown(
                f'<div class="log-entry">{entry["from"]} <span class="log-arrow">→</span> {entry["to"]}</div>',
                unsafe_allow_html=True,
            )

# ── Main area ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    user_idea = st.text_area(
        "💡 Your Story Idea",
        placeholder="e.g. A cyberpunk detective discovers memories can be stolen…",
        height=100,
    )

with col_right:
    st.markdown("<br>", unsafe_allow_html=True)
    example_prompts = [
        "A cyberpunk detective discovers memories can be stolen.",
        "Write a dark fantasy story about a cursed king.",
        "A survival story on Mars with psychological horror.",
    ]
    st.markdown("**Quick ideas:**")
    for p in example_prompts:
        if st.button(p, key=p, use_container_width=True):
            st.session_state["_prefill"] = p
            st.rerun()

# handle prefill
if "_prefill" in st.session_state:
    user_idea = st.session_state.pop("_prefill")

go = st.button("🚀  Build My Story", use_container_width=True, type="primary")

if go:
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not user_idea or not user_idea.strip():
        st.warning("Please enter a story idea.")
    else:
        try:
            planner_exec, char_exec, world_exec, scene_exec = build_agents(api_key)
            st.markdown("---")
            run_pipeline(user_idea, planner_exec, char_exec, world_exec, scene_exec)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#555;font-size:0.8rem;'>"
    "Multi-Agent Story Builder · Powered by LangChain + OpenAI · WeCloudData</p>",
    unsafe_allow_html=True,
)
