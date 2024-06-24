from pybtex.database.input import bibtex

def get_personal_data():
    name = ["Supreeth", "Narasimhaswamy"]
    email = "supreeth.narasimhaswamy@gmail.com"
    github = "SupreethN"
    linkedin = "supreeth-n"
    bio_text = f"""
                <p>
                    I am a researcher at Adobe Applied Research (GenAI) working on computer vision, machine learning, and generative modeling.
                    Prior to joining Adobe, I was a PhD student in <a href="https://www3.cs.stonybrook.edu/~cvl/" target="_blank">CVLab</a> at the <a href="https://www.cs.stonybrook.edu" target="_blank">Stony Brook University (New York, US)</a> supervised by <a href="https://www3.cs.stonybrook.edu/~minhhoai/" target="_blank">Prof. Minh Hoai</a>.
                    As an undergraduate student, I studied Computer Science at the <a href="https://www.rvce.edu.in" target="_blank">RV College of Engineering (Bengaluru, India)</a>.
                </p>
                <p>For any inquiries, feel free to reach out to me via mail!</p>
                <p>
                    <a href="https://SupreethN.github.io/assets/other/bio.txt" target="_blank" style="margin-right: 5px"><i class="fa-solid fa-graduation-cap"></i> Bio</a>
                    <a href="https://SupreethN.github.io/assets/pdf/CV_Supreeth_Narasimhaswamy.pdf" target="_blank" style="margin-right: 5px"><i class="fa fa-address-card fa-lg"></i> CV</a>
                    <a href="mailto:supreeth.narasimhaswamy@gmail.com" style="margin-right: 5px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="https://scholar.google.com/citations?user=ZKOwfCwAAAAJ&hl=en" target="_blank" style="margin-right: 5px"><i class="fa-solid fa-book"></i> Scholar</a>
                    <a href="https://github.com/SupreethN" target="_blank" style="margin-right: 5px"><i class="fab fa-github fa-lg"></i> Github</a>
                    <a href="https://www.linkedin.com/in/supreeth-n" target="_blank" style="margin-right: 5px"><i class="fab fa-linkedin fa-lg"></i> LinkedIn</a>
                </p>
    """
    footer = """
            <div class="col-sm-12" style="">
                <h4>Webpage Template</h4>
                <p>
                    This website is based on a <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">template</a> from Michael Niemeyer. <br>
                </p>
            </div>
    """
    return name, bio_text, footer

def get_author_dict():
    return {
        }

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='Supreeth Narasimhaswamy', add_links=True):
    links = get_author_dict() if add_links else {}
    s = ""
    for p in persons:
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{make_bold_name}</span>'
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    if 'award' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <br>"""

    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'html': 'Project Page', 'pdf': 'Paper', 'supp': 'Supplemental', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')

    cite = "<pre><code>@InProceedings{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year']:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    s += " /" + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Expand bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s


def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_paper_entry(k, bib_data.entries[k])
    return s


def get_index_html():
    pub = get_publications_html()
    name, bio_text, footer = get_personal_data()
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <title>{name[0] + ' ' + name[1]}</title>
  <link rel="icon" type="image/x-icon" href="assets/beach.jpg">
</head>

<body>
    <div class="container">
        <div class="row">
            <div class="col-md-1"></div>
            <div class="col-md-10">
                <div class="row" style="margin-top: 3em;">
                    <div class="col-sm-12" style="margin-bottom: 1em;">
                    <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
                    </div>
                    <br>
                    <div class="col-md-9" style="">
                        {bio_text}
                    </div>
                    <div class="col-md-3" style="">
                        <img src="assets/img/profile.jpg" class="img-thumbnail" width="400px" alt="Profile picture">
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>News</h4>
                        <ul style="line-height:1.5;">
                            <li><span style="background-color: yellow;">[Feb. 2024]</span> Our work on generating plausible hands in diffusion-based text-to-image models is accepted to CVPR, 2024. </li>
                            <li><span style="background-color: yellow;">[Feb. 2024]</span> Our work on segmenting and tracking hand-held objects is accepted to CVPR, 2024. </li>                         
                            <li>[Feb. 2024] I joined Adobe Applied Research (GenAI) as a full-time researcher. </li>
                            <li>[Feb. 2024] I successfully defended my PhD! This has been a fantastic journey! </li>
                            <li>[Dec. 2023] I completed a research internship at Adobe Research.</li>
                            <li>[Sep. 2023] Our preliminary work on diffusion-based hand generation is accepted at ICCV 2023 Hands Workshop.</li>
                            <li>[Oct. 2022] I talked about our work on hand analysis at Adobe Research. Thanks <a href="https://research.adobe.com/person/yi-zhou/" target="_blank" style="color:#334AFF;">Yi Zhou</a> and <a href="https://research.adobe.com/person/yang-zhou/" target="_blank" style="color:#334AFF;">Yang Zhou</a> for hosting.</li>
                            <li>[Sep. 2022] I completed a research internship at Snap Research, NYC. </li>
                            <li>[Jul. 2022] I gave a talk about our work on hand analysis at the Max Planck Institute for Intelligent Systems. Thanks <a href="https://ps.is.mpg.de/person/sdwivedi" target="_blank" style="color:#334AFF;">Sai Dwivedi</a>, <a href="https://ps.is.mpg.de/~dtzionas" target="_blank" style="color:#334AFF;">Dimitrios Tzionas</a>, and <a href="https://ps.is.mpg.de/~black" target="_blank" style="color:#334AFF;">Michael Black</a> for hosting.</li>
                            <li>[Mar. 2022] Two papers @ CVPR: Our work on hand-body association and hand tracking are accepted to CVPR 2022.</li>
                            <li>[Aug. 2021] I completed a research internship at Microsoft.</li>
                            <li>[Sep. 2020] Our work on joint hand detection and contact recognition is accepted to NeurIPS, 2020.</li>
                            <li>[Jul. 2019] Our work on detecting hands in unconstrained environments is accepted to ICCV, 2019.</li>
                            <li>[Jul. 2019] Our work on hand interactions in manual assembly settings is accepted to BMVC, 2019.</li>
                            <li>[Aug. 2018] I started my graduate studies at the Department of Computer Science, Stony Brook University.</li>
                        </ul>
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Publications</h4>
                        {pub}
                    </div>
                </div>
                <div class="row" style="margin-top: 3em; margin-bottom: 1em;">
                    {footer}
                </div>
            </div>
            <div class="col-md-1"></div>
        </div?
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>

</html>
    """
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')