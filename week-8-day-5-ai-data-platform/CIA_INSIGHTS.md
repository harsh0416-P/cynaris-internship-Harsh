# CIA Mentor Insights — W8D5

## Q1. Additional Data-Quality Checks

The mentor recommended these checks before trusting business insights:

- Correct data types
- Range and domain validation
- Outlier detection
- Cross-field consistency
- Date sanity checks
- Unique business keys
- Standardized categorical values
- Whitespace and invisible-character checks
- Encoding validation
- Distribution checks against market benchmarks
- Temporal drift detection
- Referential integrity

## Q2. Making the EDA Workflow Reproducible

Recommended workflow:

Raw Data → Data Validation → Clean Data → Parameterized Notebook → Automated HTML Report → Version Control and CI

### Priority Improvements

1. Add a data-validation layer.
2. Parameterize the notebook using Papermill.
3. Automate HTML report generation using nbconvert.
4. Create a single pipeline.py entry point.
5. Add pytest tests and data versioning later.

### Medium-Effort Enhancements

- DVC for data versioning
- pytest for analytic functions
- Scheduled CI runs
- Environment configuration

### Optional Improvements

- Streamlit dashboard
- MkDocs documentation
- Audit logging and lineage

## Implementation Decision

Prioritize data validation and reproducible reporting. Treat other enhancements as future improvements.