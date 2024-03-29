"""Run or update the project. This file uses the `doit` Python package. It works
like a Makefile, but is Python-based

NOTE!!!
To complete this assignment, you must adjust this file, the dodo.py
file, so that it will call the wage_growth_analytics.py file and
save the time series data from it in the data/pulled directory.
This then feeds into the next task which will create a plot
of the time series and save the plot in the output directory.

"""
import sys
sys.path.insert(1, './src/')


import config
from pathlib import Path
from doit.tools import run_once
import os
import shutil


OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)



def task_create_adjusted_wage_growth_series():
    """ """
    file_dep = [
        "./src/load_fred.py",
        "./src/load_cps.py",
        "./src/wage_growth_analytics.py",
        ]
    targets = [DATA_DIR / "pulled" / "wage_growth.parquet"]

    return {
        "actions": [
            "ipython ./src/wage_growth_analytics.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }



def task_plot_adj_wage_growth():
    """ """
    file_dep = [DATA_DIR / "pulled" / "wage_growth.parquet"]
    targets = [OUTPUT_DIR / "adj_wage_growth.png"]

    return {
        "actions": [
            "ipython ./src/plot_adj_wage_growth.py",
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }



###########################################
## Extra: Unneeded for HW
###########################################


# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --inplace ./src/{notebook}.ipynb"
def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir={output_dir} ./src/{notebook}.ipynb"
def jupyter_to_python(notebook, build_dir):
    """Convert a notebook to a python script"""
    return f"jupyter nbconvert --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"
def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"
# fmt: on



# # Check if .env file exists. If not, create it by copying from .env.example
# env_file = ".env"
# env_example_file = "example.env"

# if not os.path.exists(env_file):
#     shutil.copy(env_example_file, env_file)




def task_convert_notebooks_to_scripts():
    """Preps the notebooks for presentation format.
    Execute notebooks with summary stats and plots and remove metadata.
    """
    build_dir = Path(OUTPUT_DIR)
    build_dir.mkdir(parents=True, exist_ok=True)

    notebooks = [
        "01_wage_growth_during_the_recession.ipynb",
    ]
    file_dep = [Path("./src") / file for file in notebooks]
    stems = [notebook.split(".")[0] for notebook in notebooks]
    targets = [build_dir / f"_{stem}.py" for stem in stems]

    actions = [
        # *[jupyter_execute_notebook(notebook) for notebook in notebooks_to_run],
        # *[jupyter_to_html(notebook) for notebook in notebooks_to_run],
        # *[jupyter_clear_output(notebook) for notebook in stems],
        *[jupyter_to_python(notebook, build_dir) for notebook in stems],
    ]
    return {
        "actions": actions,
        "targets": targets,
        "task_dep": [],
        "file_dep": file_dep,
        "clean": True,
    }


def task_run_notebooks():
    """Preps the notebooks for presentation format.
    Execute notebooks with summary stats and plots and remove metadata.
    """
    notebooks_to_run_as_md = [
        "01_wage_growth_during_the_recession.ipynb",
    ]
    stems = [notebook.split(".")[0] for notebook in notebooks_to_run_as_md]

    file_dep = [
        ## 01_wage_growth_during_the_recession.ipynb
        "./src/load_fred.py",
        "./src/load_cps.py",
        "./src/wage_growth_analytics.py",
        *[Path(OUTPUT_DIR) / f"_{stem}.py" for stem in stems],
    ]

    targets = [
        ## Notebooks converted to HTML
        *[OUTPUT_DIR / f"{stem}.html" for stem in stems],
    ]

    actions = [
        *[jupyter_execute_notebook(notebook) for notebook in stems],
        *[jupyter_to_html(notebook) for notebook in stems],
        # *[jupyter_clear_output(notebook) for notebook in stems],
        # *[jupyter_to_python(notebook, build_dir) for notebook in notebooks_to_run],
    ]
    return {
        "actions": actions,
        "targets": targets,
        "task_dep": [],
        "file_dep": file_dep,
        "clean": True,
    }


# def task_knit_RMarkdown_files():
#     """Preps the RMarkdown files for presentation format.
#     This will knit the RMarkdown files for easier sharing of results.
#     """
#     files_to_knit = [
#         'shift_share.Rmd',
#         ]

#     files_to_knit_stems = [file.split('.')[0] for file in files_to_knit]

#     file_dep = [
#         'load_performance_and_loan_merged.py',
#         *[file + ".Rmd" for file in files_to_knit_stems],
#         ]

#     file_output = [file + '.html' for file in files_to_knit_stems]
#     targets = [OUTPUT_DIR / file for file in file_output]

#     def knit_string(file):
#         return f"""Rscript -e 'library(rmarkdown); rmarkdown::render("{file}.Rmd", output_format="html_document", OUTPUT_DIR="../output/")'"""
#     actions = [knit_string(file) for file in files_to_knit_stems]
#     return {
#         "actions": [
#                     "module use -a /opt/aws_opt/Modulefiles",
#                     "module load R/4.2.2",
#                     *actions],
#         "targets": targets,
#         'task_dep':[],
#         "file_dep": file_dep,
#     }


# def task_compile_latex_docs():
#     """Example plots"""
#     file_dep = [
#         "./reports/report_example.tex",
#         "./reports/slides_example.tex",
#         "./src/example_plot.py",
#         "./src/example_table.py",
#     ]
#     file_output = [
#         "./reports/report_example.pdf",
#         "./reports/slides_example.pdf",
#     ]
#     targets = [file for file in file_output]

#     return {
#         "actions": [
#             "latexmk -xelatex -cd ./reports/report_example.tex",  # Compile
#             "latexmk -xelatex -c -cd ./reports/report_example.tex",  # Clean
#             "latexmk -xelatex -cd ./reports/slides_example.tex",  # Compile
#             "latexmk -xelatex -c -cd ./reports/slides_example.tex",  # Clean
#             # "latexmk -CA -cd ../reports/",
#         ],
#         "targets": targets,
#         "file_dep": file_dep,
#         "clean": True,
#     }
