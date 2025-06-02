# Global Rule: Prioritize Modularity and Extensibility in Design

When designing new projects, modules, or undertaking major refactoring, I (Cline) will explicitly:

1.  **Discuss and Prioritize Modular Design:**
    *   Advocate for breaking down complex systems into smaller, independent, and reusable modules.
    *   Emphasize clear separation of concerns (SoC) for each module.

2.  **Promote Extensibility:**
    *   Suggest patterns and techniques that facilitate future enhancements and additions with minimal disruption to existing code. This includes:
        *   **Plugin Architectures:** Where appropriate, propose ways for functionalities to be added as plugins.
        *   **Clear API Boundaries:** Define stable interfaces between modules or components.
        *   **Configuration-Driven Behavior:** Favor external configuration over hardcoded logic for adaptable features.
        *   **Abstract Base Classes (ABCs) / Interfaces:** Encourage their use to define contracts for extensible components.
        *   **Dependency Injection:** Suggest its use to decouple components and improve testability and flexibility.

3.  **Consider Long-Term Maintainability:**
    *   Highlight how modular and extensible designs contribute to easier debugging, testing, and long-term maintenance.

**Rationale:**
This rule aligns directly with the principles of Module 1 ("Re-evaluating Foundations for Extensibility") from the "Envisioning Text Analyzer Advancements" roadmap and reinforces the `11-code-architecture-principles.md` global rule. It ensures that we consistently build systems that are robust, adaptable, and easier to evolve over time.

## Related Rules
- [11-code-architecture-principles.md](11-code-architecture-principles.md)
