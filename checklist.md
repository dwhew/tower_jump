# Project Development Checklist

This checklist tracks the development of the Tower Jump and Transit Detection project. It is structured to first create a minimal working example, and then to iteratively add more advanced features in a `dev` branch.

---

### Phase 1: Project Scaffolding & Setup

This phase establishes a clean, organized, and ready-to-use repository structure.

-   [x] **Task 1: Initialize Repository Structure**
    -   [x] Create the main project directory.
    -   [x] Initialize a Git repository (`git init`).
    -   [x] Add core documentation: `agent.md`, `project_overview.md`, `README.md`.
    -   [x] Create a standard Python `.gitignore` file.
    -   [x] Create the initial directory structure.

-   [x] **Task 2: Set Up Environment**
    -   [x] Create a `requirements.txt` file.
    -   [x] Add initial dependencies to `requirements.txt`.

---

### Phase 2: Minimal Working Example (MWE)

This phase focuses on creating a simple, end-to-end version of the analysis pipeline using the provided test data.

-   [ ] **Task 3: Implement Basic Preprocessing**
    -   [x] Create `src/data_models.py`.
    -   [x] Implement `load_and_standardize_data` function.
    -   [x] Add basic noise filtering.

-   [ ] **Task 4: Implement Baseline Analysis**
    -   [ ] Implement a simple tower jump detection algorithm (e.g., based on a fixed speed threshold).
    -   [ ] Implement a simple stay-point detection algorithm (e.g., based on fixed distance and time thresholds).
    -   [ ] Implement basic transit detection between stay-points.

-   [ ] **Task 5: Create Unit Tests for MWE**
    -   [ ] Write unit tests for the basic preprocessing functions.
    -   [ ] Write unit tests for the baseline analysis functions.

---

### Phase 3: Advanced Feature Development (`dev` branch)

This phase focuses on implementing the advanced, probabilistic methods from `methods_analysis.md` in a separate `dev` branch.

-   [ ] **Task 6: Create `dev` branch**
    -   [ ] Create and switch to a new `dev` branch for advanced feature development.

-   [ ] **Task 7: Implement Probabilistic Modeling**
    -   [ ] Implement probabilistic modeling of location points (2D Gaussian distributions).
    -   [ ] Implement uncertainty-aware velocity calculation using Monte Carlo simulation.
    -   [ ] Implement the "Impossible Travel" paradigm for tower jump detection.
    -   [ ] Implement the probabilistic DBSCAN (FDBSCAN) for stay point detection.

-   [ ] **Task 8: Implement Advanced Confidence Scoring**
    -   [ ] Implement the multi-factor confidence score for tower jumps.
    -   [ ] Implement the confidence score for stay points.
    -   [ ] Implement the confidence score for transit corridors.

---

### Phase 4: Integration, Validation, and Benchmarking

This phase focuses on integrating the advanced features, and then validating and benchmarking the final system.

-   [ ] **Task 9: Integrate Advanced Features**
    -   [ ] Merge the `dev` branch into `main` after thorough testing.

-   [ ] **Task 10: Comprehensive Testing**
    -   [ ] Write integration tests to validate the end-to-end pipeline.

-   [ ] **Task 11: Validation and Benchmarking**
    -   [ ] Create a ground truth dataset.
    -   [ ] Define and implement performance metrics (F1-score, Jaccard Index).
    -   [ ] Perform parameter tuning and validation.
