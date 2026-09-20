API Reference
=============

The public API is organized around submission normalization, document parsing,
automated analysis, and report generation.  The sections below expose the
main implementation modules and their Google-style docstrings.

Domain models
-------------

.. automodule:: assessment_pipeline.models
   :members:
   :show-inheritance:

Submission processing
---------------------

.. automodule:: assessment_pipeline.extractor
   :members:
   :show-inheritance:

.. automodule:: assessment_pipeline.moodle
   :members:
   :show-inheritance:

.. automodule:: assessment_pipeline.normalizer
   :members:
   :show-inheritance:

.. automodule:: assessment_pipeline.parser_registry
   :members:
   :show-inheritance:

Task detection
--------------

.. automodule:: assessment_pipeline.task_detector
   :members:
   :show-inheritance:

.. automodule:: assessment_pipeline.task_splitter
   :members:
   :show-inheritance:

Analysis and model services
---------------------------

.. automodule:: assessment_pipeline.ai_detection
   :members:

.. automodule:: assessment_pipeline.gpt_oss_client
   :members:
   :show-inheritance:

.. automodule:: assessment_pipeline.llm_pipeline
   :members:

Reporting
---------

.. automodule:: assessment_pipeline.reporting
   :members:
   :show-inheritance:

.. automodule:: assessment_pipeline.cohort_summary
   :members:

.. automodule:: assessment_pipeline.dt_adoption
   :members:

.. automodule:: assessment_pipeline.ai_usage_report
   :members:
