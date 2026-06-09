#!/usr/bin/env nextflow

nextflow.enable.dsl=2

params.input = params.input ?: "data/example"
params.out   = params.out   ?: "results"

Channel
    .fromPath("${params.input}/*")
    .map{ file -> file } 
    .set { input_files_ch }

// Create explicit channels for the two example files we expect in the demo input folder
input_files_ch
    .filter { it.name ==~ /synthetic_AllOfUs\\.csv/ }
    .set { clinical_file_ch }

input_files_ch
    .filter { it.name ==~ /HMP_resistome_demo\\.csv/ }
    .set { resistome_raw_ch }

workflow {

    preprocess_out = preprocess(clinical_file_ch, resistome_raw_ch)

    clinical_table_ch = preprocess_out[0]
    resistome_raw_ch2 = preprocess_out[1]

    res_table_ch = resistome_profile(resistome_raw_ch2)

    index_ch = build_index(res_table_ch, clinical_table_ch)

    report(index_ch)
}

process preprocess {
    tag "preprocess"
    input:
      path clinical_file
      path resistome_file
    output:
      path 'clinical_table.csv'    emit: clinical_table
      path 'resistome_raw.csv'     emit: resistome_raw
    script:
    """
    mkdir -p staging
    cp ${clinical_file} clinical_table.csv
    cp ${resistome_file} resistome_raw.csv
    """
}

process resistome_profile {
    tag "resistome_profile"
    input:
      path res_raw
    output:
      path 'resistome_table.csv' emit: res_table
    script:
    """
    # demo: pass-through (replace with RGI/DeepARG wrapper for real profiling)
    cp ${res_raw} resistome_table.csv
    """
}

process build_index {
    tag "build_index"
    input:
      path res_table
      path clin_table
    output:
      path 'resilience_index.csv' emit: index_csv
    script:
    """
    python3 scripts/build_index.py --resistome ${res_table} --clinical ${clin_table} --out resilience_index.csv
    """
}

process report {
    tag "report"
    input:
      path index_csv
    output:
      path "${params.out}"
    script:
    """
    mkdir -p ${params.out}/report
    python3 scripts/make_report.py --index ${index_csv} --out ${params.out}/report/resilience_summary.html
    cp ${index_csv} ${params.out}/resilience_index.csv
    """
}
