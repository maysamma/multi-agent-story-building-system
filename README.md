# 🤖 Multi-Agent Creative Story Building System

An advanced, orchestration-driven Multi-Agent Generative AI system designed to collaborate, brainstorm, and author cohesive, structured, and highly creative fictional stories from a single user-provided premise. Built using **LangChain** and **LangGraph**, this system coordinates six specialized digital agents with strict role boundaries and customized tools to eliminate common LLM storytelling pitfalls such as plot inconsistencies, narrative drift, and loss of historical context.

---

## 🌟 Key Features

* **Specialized Multi-Agent Architecture**: Orchestrates 6 independent agents working sequentially and iteratively to transition a raw idea into a publication-ready story chapter.
* **Role-Specific Boundary Enforcement**: Strict prompt boundaries ensure agents focus exclusively on their core expertise (e.g., the Story Planner only outlines, the Scene Writer only dramatizes) to avoid cognitive overlap.
* **Shared Story Memory & Graph State**: Implements a centralized state mechanism (`Story Memory` and `Lore Lookup`) that enables asynchronous information retrieval, preventing chronological or character-trait contradictions across longer texts.
* **Iterative Critique & Refinement Loop**: Features an automated critique-correction cycle between the `Consistency Checker` and `Scene Writer` to autonomously identify and patch narrative plotholes before formatting.

---

## 🏗️ System Architecture & Workflow

The system takes a simple user prompt (e.g., *"A cyberpunk detective discovers memories can be stolen."*) and guides it through an automated 8-step pipeline:
