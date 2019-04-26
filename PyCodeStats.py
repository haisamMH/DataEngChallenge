from github import Github

import urllib.request

import re

import ssl

import sys

from concurrent.futures import ThreadPoolExecutor



gcontext = ssl.SSLContext()

g = Github("UmerF920", "clegane1992", base_url="https://api.github.com")





"""

Func: get_stats_from_a_repo



input params:

repository_url: String



output:

result: dict [containing the statistics of the repository]

"""



def get_stats_from_a_repo(repository_url):



    try:

        # Initial variables to calculate the stats

        line_count = 0

        imports = []

        func_params = []

        variables = 0

        loop_depths = []

        depth_level = 0

        loop_start_spaces = 0

        current_spaces = 0

        duplicates = []



        # Get the part of repo from the url which will be used to fetch its components

        repo = g.get_repo(str(repository_url.split(".com/", 1)[1].rstrip("\n\r")))



        # Get all contents from the repo thus the empty string a param

        contents = repo.get_contents("")



        while len(contents) > 1:

            file_content = contents.pop(0)

            if file_content.type == "dir": # Open up further if it is a directory

                contents.extend(repo.get_contents(file_content.path))

            elif file_content.download_url:

                if file_content.download_url.endswith(".py"): # If we have found a code file

                    all_code_lines = []

                    for line in urllib.request.urlopen(file_content.download_url, context=gcontext): # Loading the file from remote url

                        string_line = line.decode("utf-8") # Converting the encoded line into string making it readable for the python code





                        """

                        Checking if it is a real line of code, all empty lines are ignored,

                        multi-line comments not supported

                        """

                        if string_line and string_line[0] != "\n" and string_line.lstrip() and \

                                    string_line.lstrip()[0] != "#":

                            all_code_lines.append(string_line.replace(" ", "").split('#', 1)[0].rstrip("\n\r"))

                            if string_line.lstrip().partition(' ')[0] == "import" or \

                                        string_line.lstrip().partition(' ')[0] == "from":

                                imports.append(

                                    string_line.lstrip().split(' ', 1)[1].rstrip("\n\r").split(' ', 1)[0])

                            if " = " in string_line:

                                variables += 1

                            line_count += 1



                            """

                            To calculate the nesting factor if a loop is found

                            initial starting point is saved and the end of loop

                            is searched

                            """



                            if string_line.lstrip().partition(' ')[0] == "for": # If there is a loop in this line

                                if depth_level == 0: # Start of a loop found

                                    depth_level += 1

                                    current_spaces = len(string_line) - len(string_line.lstrip())

                                    loop_start_spaces = current_spaces # Saving current depth of the nesting factoring

                                else:

                                    new_spaces = len(string_line) - len(string_line.lstrip()) # Checking for new depth of nesting factor

                                    if new_spaces > current_spaces:

                                        current_spaces = new_spaces

                                        depth_level += 1



                            # Check if the outer most loop has ended

                            if len(string_line) - len(string_line.lstrip()) <= loop_start_spaces and depth_level > 0 \

                                and string_line.lstrip().partition(' ')[0] != "for":

                                loop_depths.append(depth_level)

                                depth_level = 0



                        # Function definition found

                        if string_line.lstrip().partition(' ')[0] == "def":

                            params = string_line.split('(', 1)[1].split(')', 1)[0]

                            # Catch the params in the definition

                            if params:

                                func_params.append(len(string_line.split('(', 1)[1].split(')', 1)[0].split(',')))

                            else:

                                func_params.append(0)



                    """

                    Take a chunk of four lines every time and then look for it

                    in the rest of the file

                    """

                    for i in range(0, len(all_code_lines)):

                        duplication = 0

                        four_lines = []

                        if i + 4 <= len(all_code_lines):

                            for j in range(i, i + 4):

                                four_lines.append(all_code_lines[j])

                            """

                            Sum the matches found for 4 lines chunk and decrement by 1

                            to make sure that chunk is not matching to itself

                            """

                            duplication = sum(

                                all_code_lines[k:k + len(four_lines)] == four_lines for k in range(len(all_code_lines))) - 1

                        if duplication > 0:

                            duplicates.append(duplication)



                # If the file ends with a loop then add this depth_level for nesting factor

                if depth_level > 0:

                    loop_depths.append(depth_level)

                    depth_level = 0







        # Calculating stats from raw results

        duplication_avg = 0

        if len(duplicates) > 0:

            duplication_avg = sum(duplicates)/len(duplicates)



        func_params_avg = 0

        if len(func_params) > 0:

            func_params_avg = sum(func_params)/len(func_params)



        nesting_factor = 0

        if len(loop_depths) > 0:

            nesting_factor = sum(loop_depths)/len(loop_depths)



        average_variables = 0

        if line_count > 0:

            average_variables = variables / line_count



        # Creating a dictionary of results for the repository

        result = {

            'repository_url': repository_url.rstrip("\n\r"),

            'number of lines': line_count,

            'libraries': imports,

            'nesting factor': nesting_factor,

            'code duplication': duplication_avg,

            'average parameters': func_params_avg,

            'average variables': average_variables

        }



        # return the resultant statistics for the repo

        return result

    except:

        return {

            'repository_url': repository_url.rstrip("\n\r"),

            'status': 'unable to process with repo'

        }





# The file to read all the repository URLs from

repos_list = urllib.request.urlopen("https://raw.githubusercontent.com/monikturing/turing-data-challenge/master/url_list.csv", context=gcontext)



# First line of the file is a header, so to ignore it

next(repos_list)



master_stats = []



output_file = open("output.txt", "w")

output_file.write("[")

# Create a pool of threads to carry out the complete job, pool size is random

with ThreadPoolExecutor(max_workers=25) as executor:

    for repo in repos_list:

        if repo.decode("utf-8") != "https://github.com/braingineer/ikelos\n" and \

                        repo.decode("utf-8") != "https://github.com/congresso-em-numeros/congresso\n" and \

                        repo.decode("utf-8") != "https://github.com/bjut-hz/SAO\n":

            print("=== Repository Url ===")

            print(repo.decode("utf-8"))

            stats = executor.submit(get_stats_from_a_repo, repo.decode("utf-8")).result()

            output_file.write(str(stats) + ",\n")

            master_stats.append(stats)

output_file.write("]")

output_file.close()
