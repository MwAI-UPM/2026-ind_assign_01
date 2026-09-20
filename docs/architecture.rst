Architecture
============

The assessment pipeline transforms heterogeneous student submissions into
structured, reviewable cohort-level evidence.  It preserves the original
submission content in a normalized JSON representation, applies automated
analysis and evaluation, and produces CSV reports that can be consumed by a
teaching dashboard.

End-to-end flow
---------------

The implemented flow is:

.. code-block:: mermaid

   flowchart LR

       A[Raw Submissions<br/>PDF DOCX XLSX]

       A --> B[Normalization]

       B --> C[data/normalized]

       C --> D[Analysis<br/>analyze_all.py]

       D --> E[GPT Analysis]

       D --> F[AI Detection]

       E --> G[data/analysis]

       F --> G

       G --> H[Evaluation<br/>evaluate_all.py]

       H --> I[data/evaluation]

       G --> J[Cohort Summary]

       I --> J

       C --> K[Digital Twin Detection]

       G --> K

       G --> L[AI Usage Report]

       J --> M[Teaching Dashboard]
       K --> M
       L --> M

The final dashboard is an intended consumer of the generated CSV products;
this repository currently supplies the data products rather than a dashboard
application itself.

Pipeline stages
---------------

Raw submissions and normalization
    ``process_all.py`` scans the Moodle export directory, discovers student
    submissions, extracts text from supported document formats, identifies
    assignment sections, and serializes one JSON record per student in
    ``data/normalized/<student_id>.json``.  The normalized record contains
    student metadata, source-document metadata, extracted text, character
    counts, and task information.  This is the canonical input for all later
    stages.

Analysis
    ``analyze_all.py`` reads the normalized JSON files.  It constructs two
    views of each submission: an 8,000-character reduced payload sent to the
    local GPT-OSS service for structured classification, and an untruncated
    text corpus retained for deterministic detection.  The model identifies
    document structure, assignment type, detected tasks, completeness,
    summary, issues, and declared AI use.  Results are written to
    ``data/analysis/<student_id>_analysis.json``.

AI detection
    AI-tool detection is deterministic and keyword-based.  It scans the full
    normalized text for configured names and terms such as ChatGPT, Claude,
    Copilot, Gemini, Perplexity, LLM, and generative AI.  The detected labels
    and the detection method are added to the analysis record.  This detects
    explicit textual mentions; it is not authorship attribution or proof that
    a tool was used.

Evaluation
    ``evaluate_all.py`` sends each analysis record, rather than the original
    submission, to the evaluation prompt.  The evaluator produces structured
    completeness, quality, evidence-strength, and confidence values together
    with strengths, weaknesses, recommendations, and an evaluation summary.
    Records are written to ``data/evaluation/<student_id>_evaluation.json``.

Cohort summary
    ``cohort_summary.py`` joins analysis and evaluation records for students
    that have both files.  It produces ``data/cohort_summary.csv`` with one
    row per student and fields for assignment type, detected tasks,
    completeness, quality, evidence strength, confidence, and AI-use data.
    This is the principal compact input for cohort-level visualization.

Digital Twin detection
    ``dt_adoption.py`` combines normalized submission text with analysis and
    evaluation records.  It first checks whether enough tasks were completed
    for the submission to be evaluated, then classifies Digital Twin content
    as ``DT_recommended``, ``DT_mentioned``, ``DT_not_found``, or
    ``DT_not_evaluable``.  It also stores a short textual evidence excerpt in
    ``data/dt_adoption.csv``.  The classification is rule-based and should be
    interpreted as an adoption signal, not a semantic assessment of the
    proposal.

AI usage report
    ``ai_usage_report.py`` converts the AI-use fields in the analysis records
    into ``data/ai_usage_report.csv``.  It includes student identity,
    completeness, whether AI use was declared, the detected tools, and the
    supporting evidence.  Like the analysis field, this report records
    explicit declarations or textual mentions and does not infer undisclosed
    use.

Generated artifacts
-------------------

The pipeline uses a file-based contract between stages:

``data/normalized``
    Canonical per-student submissions with extracted text and metadata.

``data/analysis``
    Per-student GPT-OSS classifications enriched with deterministic AI-use
    detection.

``data/evaluation``
    Per-student quality and evidence evaluations derived from the analysis.

``data/cohort_summary.csv``
    Joined cohort-level analysis and evaluation metrics.

``data/dt_adoption.csv``
    Digital Twin status and evidence for each evaluable submission.

``data/ai_usage_report.csv``
    Explicit AI-use declarations, detected tools, and supporting evidence.

Execution order
---------------

Run the stages in dependency order from the project root:

1. ``python -m assessment_pipeline.process_all``
2. ``python -m assessment_pipeline.analyze_all``
3. ``python -m assessment_pipeline.evaluate_all``
4. ``python -m assessment_pipeline.cohort_summary``
5. ``python -m assessment_pipeline.dt_adoption``
6. ``python -m assessment_pipeline.ai_usage_report``

The analysis and evaluation stages require access to the configured local
GPT-OSS endpoint.  The reporting stages depend on the JSON files produced by
the preceding stages and can be rerun without reprocessing the source
submissions.
