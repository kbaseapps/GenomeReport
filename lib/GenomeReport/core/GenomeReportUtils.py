import os
import uuid
import errno
import time

from installed_clients.GenomeAnnotationAPIClient import GenomeAnnotationAPI
"""
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
"""
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace as workspaceService


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages.
    """
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time())
          + ': ' + message)


def _mkdir_p(path):
    """
    _mkdir_p: make directory for given path
    """
    if not path:
        return
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class GenomeReportUtils:

    def __init__(self, config):
        self.scratch = config["scratch"]
        self.ctx = config['ctx']
        self.callback_url = config["SDK_CALLBACK_URL"]

        self.ws_client = workspaceService(config["workspace-url"])
        self.kbr = KBaseReport(self.callback_url)
        self.genome_api = GenomeAnnotationAPI(self.callback_url)
        """
        self.gfu = GenomeFileUtil(self.callback_url)
        self.au = AssemblyUtil(self.callback_url)
        self.dfu = DataFileUtil(self.callback_url)
        """
        self.output_workspace = None

    def upload_file(self, filepath, message="Annotation report generated by kb_prokka"):
        """
        Upload a file to shock
        :param filepath: File to upload
        :param message: Optional Upload Message
        :return:
        """
        output_file_shock_id = self.dfu.file_to_shock({"file_path": filepath})["shock_id"]
        print(f"Uploaded filepath {filepath} to shock and got id {output_file_shock_id}")
        return {"shock_id": output_file_shock_id,
                "name": os.path.basename(filepath),
                "label": os.path.basename(filepath),
                "description": message}

    def _write_genome_js(self, js_template):  # , out_dir, dt_info):
        """
        _write_genome_js: Generate the js script that handles the data presentation and interaction
        """
        log('start writing js script...')
        js_content = '<script>'
        with open(os.path.join(os.path.dirname(__file__), js_template)) as js_file:
            js_content += js_file.read()
        js_content += '</script>'

        # log(f'The report js script is:\n {js_content}')
        return js_content

    def _generate_genome_html(self, out_dir, genome_ref):
        """
        _generate_genome_html: generate html report on genome
        """
        log('start generating html report')
        genome_obj = self.genome_api.get_genome_v1(
            {"genomes": [{"ref": genome_ref}], 'downgrade': 0, 'no_data': 0, 'no_metadata': 0}
            )["genomes"][0]
        curr_func = len(genome_obj["data"]["features"])
        # log(f'feature_counts: {genome_obj['data']['feature_counts']}, CDS count={curr_func}')

        genome_name = genome_obj['info'][1]
        report_title = f'Genome report on {genome_name}'

        html_report = list()
        report_file_path = os.path.join(out_dir, 'genome_report.html')

        header_content = f'<header><h3>Genome Report-{genome_name}</h3></header>'
        js_content1 = self._write_genome_js('line_chart.js')
        js_content2 = self._write_genome_js('pie_chart.js')
        js_content3 = self._write_genome_js('bar_chart_anim.js')
        summ_content = (
            f'<div id="brief_description">\n'
            f'Genome {genome_name} was created by {genome_obj["creator"]} on {genome_obj["created"]}.'
            f'Path is {genome_obj["path"]}, orig_wsid={genome_obj["orig_wsid"]}.'
            f'<br>Taxonomy:{genome_obj["info"][10]["Taxonomy"]}.'
            f'<br>Details of the analysis, including genes of interest (Specialty Genes),'
            f'a functional categorization (Subsystems), and a phylogenetic tree'
            f'(Phylogenetic Analysis) are provided below.'
            f'</div>')
        footer_content = ''
        with open(os.path.join(os.path.dirname(__file__), 'citations.html'), 'r') as footer_file:
            footer_content = footer_file.read()

        header_placeholder = '<header><h3 id="report_header_placeholder"></h3></header>'
        summary_placeholder = '<div id="brief_description"></div>'
        js_placeholder1 = '<script src="javascript_placeholder1.js"></script>'
        js_placeholder2 = '<script src="javascript_placeholder2.js"></script>'
        js_placeholder3 = '<script src="javascript_placeholder3.js"></script>'
        footer_placeholder = '<div id="report_footer_placeholder"></div>'

        with open(report_file_path, 'w') as report_file:
            with open(os.path.join(os.path.dirname(__file__), 'genome_report_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace(header_placeholder, header_content)
                report_template = report_template.replace(summary_placeholder, summ_content)
                report_template = report_template.replace(js_placeholder1, js_content1)
                report_template = report_template.replace(js_placeholder2, js_content2)
                report_template = report_template.replace(js_placeholder3, js_content3)
                report_template = report_template.replace(footer_placeholder,
                                                          f'<div>{footer_content}</div>')
                report_file.write(report_template)
                log(f'The report with js script is:\n {report_template}')

        html_report.append({'path': report_file_path,
                            'name': os.path.basename(report_file_path),
                            'label': os.path.basename(report_file_path),
                            'description': 'Genome report with table(s) and/or chart(s)'})

        return (html_report, curr_func, report_title)

    def report_genome(self, params, html_links=[]):
        """ Create report output with (reannotated) assembly/genome, and some stats
        :param genome: (reannotated) Genome Reference, Report Files and Stats
        :return: Reference to Report Object
        """
        self.output_workspace = params['output_workspace']
        genome_ref = params['object_ref']

        if params['annotated_by']:
            ann_by = params['annotated_by']
        else:
            ann_by = ''

        report_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        _mkdir_p(report_dir)
        html_files, curr_func, rpt_title = self._generate_genome_html(report_dir, genome_ref)

        if params.get('gn_stats', None):
            genome_stats = params['gn_stats']
        else:
            genome_stats = {"current_functions": curr_func, "new_functions": 0,
                            "found_functions": 0, "new_ontologies": 0}

        html_links += html_files

        # file_links = [self.upload_file(genome.ontology_summary_filepath, ann_by),
        #              self.upload_file(genome.function_summary_filepath, ann_by)]

        report_message = (f"Genome Ref: {genome_ref}"
                          f"Number of features: {genome_stats['current_functions']}"
                          f"New functions found:{genome_stats['new_functions']}"
                          f"Ontology terms found:{genome_stats['new_ontologies']}")

        report_info = self.kbr.create_extended_report(
            {"message": report_message,
             "objects_created": [{"ref": genome_ref, "description": "Input genome"}],
             # "file_links": file_links,
             'html_links': html_files,
             'direct_html_link_index': 0,
             'html_window_height': 366,
             "report_object_name": "genome_report_" + str(uuid.uuid4()),
             "workspace_name": self.output_workspace
             })

        return {"genome_ref": genome_ref, "report_name": report_info["name"],
                "report_ref": report_info["ref"]}
