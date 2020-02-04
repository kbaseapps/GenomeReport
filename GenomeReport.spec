
/*
@author qzhang
A KBase module to specifically handle reporting on genomes
*/

module GenomeReport {
   /* A boolean. 0 = false, anything else = true. */
    typedef int boolean;
    /*
        Reference to an Assembly/Genome/GenomeAnnotation object in the workspace
        @id ws KBaseGenomeAnnotations.Assembly
        @id ws KBaseGenomes.Genome
        @id ws KBaseGenomeAnnotations.GenomeAnnotation
        @id ws KBaseGenomeAnnotations.GenomeAnnotationSummary
        @id ws KBaseMetagenomes.AnnotatedMetagenomeAssembly
    */
    typedef string data_obj_ref;
    /*
     * Workspace ID reference in the format 'workspace_id/object_id/version'
     * @id ws
     */
    typedef string ws_id;

    /* A string pointing to the genome function/ontology summary file path */
    typedef string summary_filepath;
    
    typedef structure {
        string file_shock_id;
        string file_basename;
        string file_label;
        string description;
    } file_link;

    typedef structure {
        int current_functions;
        int new_funcgtions;
        int found_functions;
        int new_ontologies;
    } genome_stats;

    /*
        Required parameters:
            object_ref - reference to Assembly or Genome object,
            output_workspace - output workspace name where the report will be saved

        Optional parameters (depending on different report templates):
            --annotated_by - the function/method used to annotate the genome
            --genomeAnnotation_summary - the object that holds the meta data of the genome annotation
            --function_summary_fp - file path to function summary,
            --ontology_summary_fp - file path to ontology summary,
            --gn_stats - an object holding the genome stats info
            --report_message - a message included in the report, default to '',
            --warnings - a warning message included in the report, default to [],
            --file_links - a list of file_link to shock files generated by other genome apps
                          (e.g., annotation apps), default to [],
            --html_links - a list of file_link to the output html files, default to [],
            --direct_html - a link to the direct html, default to ''
    */
    typedef structure {
        data_obj_ref object_ref;
        string output_workspace;
        string annotated_by;
        data_obj_ref genomeAnnotation_summary; 
        summary_filepath function_summary_fp;
        summary_filepath ontology_summary_fp;
        genome_stats gn_stats;
        string report_message;
        list<string> warnings;
        list<file_link> file_links;
        list<file_link> html_links;
        string direct_html;
    } GenomeReportParams;

    typedef structure {
        string report_name;
        string report_ref;
    } GenomeReportOutput;

    funcdef create_genome_report(GenomeReportParams params)
        returns (GenomeReportOutput output) authentication required;
};

