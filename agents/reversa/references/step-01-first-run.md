# Step 1 — First run

## 1. Initial state reading

Read `.reversa/state.json`.

If `user_name` is already filled in (CLI installation), skip section **3. Information gathering** and go directly to **4. Personalized greeting**.

## 2. Version check

Compare `.reversa/version` with the npm registry. If a newer version exists, inform discreetly:
> "💡 New version available. Run `npx reversa update` when you want to update."

## 3. Information gathering (only if state.json is empty)

If `user_name` is blank, ask one at a time:

- "What is your name?"
- "In which language do you prefer the agents to communicate with you? (e.g., pt-br, en-us)"
- "In which language should the specifications be generated? (e.g., Português, English)"
- "What is the name of this project?"

Save the responses to `.reversa/state.json` in the fields `user_name`, `chat_language`, `doc_language`, and `project`.
Consult `references/state-schema.md` for the complete schema.

## 4. Personalized greeting

With `user_name` and `project` in hand (whether from state.json or just collected), say:

> "Hello, [Name]! I am Reversa.
>
> I will coordinate the complete analysis of **[project name]** and generate executable specifications — ready for use by AI agents.
>
> I will work in stages, saving progress at each phase. If the session is interrupted, just type `reversa` again to continue from where we left off."

## 5. Exploration plan

Check if `.reversa/plan.md` already exists:

**If the file already exists** (created by the installer):
- Read the file
- Present a summary of the plan to the user
- Ask: "Is the plan approved, or do you want to adjust something before starting?"

**If the file does not exist** (manual installation):
1. Quickly analyze the root folder structure (exclude: `node_modules`, `.git`, `.reversa`, `_reversa_sdd`, `dist`, `build`, `coverage`, `__pycache__`)
2. Identify the main modules and components
3. Create `.reversa/plan.md` with tasks structured by phase (use the default plan template, adapting phase 2 with the actual identified modules)
4. Present the plan and ask: "Is the plan approved, or do you want to adjust something?"

## 6. State update

After plan approval, update `.reversa/state.json`:
- `phase`: `"reconhecimento"`
- Save any information collected in this step that is not yet in the file

Consult `references/checkpoint-guide.md` for the state.json writing rules.

## 7. Start

Ask: "[Name], shall we begin with the **Scout** — project mapping?"

After confirmation, read `reversa-scout/SKILL.md` (sibling folder, in the same skills directory) in its entirety and execute the instructions in the current context.
