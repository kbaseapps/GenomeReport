# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from pprint import pformat

from GenomeReport.core.GenomeReportUtils import GenomeReportUtils
from installed_clients.WorkspaceClient import Workspace as workspaceService
# from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class GenomeReport:
    '''
    Module Name:
    GenomeReport

    Module Description:
    @author qzhang
A KBase module to specifically handle reporting on genomes
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "HEAD"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        self.ws_client = workspaceService(config["workspace-url"])
        #END_CONSTRUCTOR
        pass


    def create_genome_report(self, ctx, params):
        """
        :param params: instance of type "GenomeReportParams" (Required
           parameters: object_ref - reference to Assembly or Genome object,
           output_workspace - output workspace name where the report will be
           saved Optional parameters (depending on different report
           templates): --annotated_by - the function/method used to annotate
           the genome --genomeAnnotation_summary - the object that holds the
           meta data of the genome annotation --function_summary_fp - file
           path to function summary, --ontology_summary_fp - file path to
           ontology summary, --stats - an object holding the genome stats
           info --report_message - a message included in the report, default
           to '', --warnings - a warning message included in the report,
           default to [], --file_links - a list of file_link to shock files
           generated by other genome apps (e.g., annotation apps), default to
           [], --html_links - a list of file_link to the output html files,
           default to [], --direct_html - a link to the direct html, default
           to '') -> structure: parameter "object_ref" of type "data_obj_ref"
           (Reference to an Assembly/Genome/GenomeAnnotation object in the
           workspace @id ws KBaseGenomeAnnotations.Assembly @id ws
           KBaseGenomes.Genome @id ws KBaseGenomeAnnotations.GenomeAnnotation
           @id ws KBaseGenomeAnnotations.GenomeAnnotationSummary @id ws
           KBaseMetagenomes.AnnotatedMetagenomeAssembly), parameter
           "output_workspace" of String, parameter "annotated_by" of String,
           parameter "genomeAnnotation_summary" of type "data_obj_ref"
           (Reference to an Assembly/Genome/GenomeAnnotation object in the
           workspace @id ws KBaseGenomeAnnotations.Assembly @id ws
           KBaseGenomes.Genome @id ws KBaseGenomeAnnotations.GenomeAnnotation
           @id ws KBaseGenomeAnnotations.GenomeAnnotationSummary @id ws
           KBaseMetagenomes.AnnotatedMetagenomeAssembly), parameter
           "function_summary_fp" of type "summary_filepath" (A string
           pointing to the genome function/ontology summary file path),
           parameter "ontology_summary_fp" of type "summary_filepath" (A
           string pointing to the genome function/ontology summary file
           path), parameter "stats" of type "genome_stats" -> structure:
           parameter "currnet_functions" of Long, parameter "new_funcgtions"
           of Long, parameter "found_functions" of Long, parameter
           "new_ontologies" of Long, parameter "report_message" of String,
           parameter "warnings" of list of String, parameter "file_links" of
           list of type "file_link" -> structure: parameter "file_shock_id"
           of String, parameter "file_basename" of String, parameter
           "file_label" of String, parameter "description" of String,
           parameter "html_links" of list of type "file_link" -> structure:
           parameter "file_shock_id" of String, parameter "file_basename" of
           String, parameter "file_label" of String, parameter "description"
           of String, parameter "direct_html" of String
        :returns: instance of type "GenomeReportOutput" -> structure:
           parameter "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN create_genome_report
        print(("Input parameters: " + pformat(params)))
        self.config['ctx'] = ctx
        self.report_util = GenomeReportUtils(self.config)
        output = self.report_util.report_genome(params)
        #END create_genome_report

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method create_genome_report return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
