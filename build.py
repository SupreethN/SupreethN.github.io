from pybtex.database.input import bibtex

def get_personal_data():
    name = ["Supreeth", "Narasimhaswamy"]
    email = "supreeth.narasimhaswamy@gmail.com"
    github = "SupreethN"
    linkedin = "supreeth-n"
    bio_text = f"""
                <p>
                    I am a Research Scientist at Luma AI, building multimodal foundation models for Physical AI and Robotics. Previously, I was a Research Scientist at Adobe, where I worked on image and video generation and editing for Adobe Firefly.
                </p>
                <p>
                    I received my PhD from <a href="https://www3.cs.stonybrook.edu/~cvl/" target="_blank">CVLab</a> at <a href="https://www.cs.stonybrook.edu" target="_blank">Stony Brook University</a>, advised by <a href="https://www3.cs.stonybrook.edu/~minhhoai/" target="_blank">Prof. Minh Hoai</a>, where I built vision models and datasets to understand how human hands contact, interact with, and grasp objects.
                </p>
                <p>
                    <a href="mailto:supreeth.narasimhaswamy@gmail.com" style="margin-right: 5px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                    <a href="https://scholar.google.com/citations?user=m4VjBbsAAAAJ&hl=en" target="_blank" style="margin-right: 5px"><i class="fa-solid fa-book"></i> Scholar</a>
                    <a href="https://github.com/SupreethN" target="_blank" style="margin-right: 5px"><i class="fab fa-github fa-lg"></i> Github</a>
                    <a href="https://www.linkedin.com/in/supreeth-n" target="_blank" style="margin-right: 5px"><i class="fab fa-linkedin fa-lg"></i> LinkedIn</a>
                </p>
    """
    footer = """
            <div class="col-sm-12">
                <p class="site-footer">Website based on a <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">template</a> by Michael Niemeyer.</p>
            </div>
    """
    headline = "Research Scientist, Luma AI &middot; Physical AI &amp; Robotics &middot; Image &amp; Video Generation"
    return name, headline, bio_text, footer

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
    fit = ' pub-thumb-contain' if entry.fields.get('thumb_fit') == 'contain' else ''
    s += f"""<img src="{entry.fields['img']}" class="pub-thumb{fit}" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""

    if 'award' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <br>"""

    if 'hide_authors' not in entry.fields.keys():
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


def get_selected_work():
    # Highlights shown above the papers. 'img' and 'video' are optional;
    # entries with neither 'img' nor 'video' get a placeholder thumbnail.
    return [
        {
            'title': 'Zero-real Agent Policy (ZAP)',
            'desc': 'A 27B open model trained only in simulation that beats state-of-the-art VLAs and matches GPT-6 Astra on a real bimanual robot, while being 3× faster and 17× cheaper per task, with zero real-world training data.',
            'role': 'Core contributor',
            'venue': 'Luma AI (CoRL 2026)',
            'video': 'assets/img/work/zap.mp4',
            'poster': 'assets/img/work/zap_poster.jpg',
        },
        {
            'title': 'Adobe Firefly Image 4',
            'desc': "Adobe's foundation text-to-image generation model, trained on a commercially safe dataset.",
            'role': 'Core contributor',
            'venue': 'Adobe, 2025',
            'img': 'assets/img/work/firefly_image4.jpg',
        },
        {
            'title': 'Layered Image Editing and Decomposition',
            'desc': 'Decomposing images into editable layers for generative editing. Users specify which objects to separate into layers, enabling precise, localized control over each object\'s attributes, size, and orientation.',
            'role': 'Core contributor',
            'venue': 'Adobe Firefly',
            'img': 'assets/img/work/layered_editing.jpg',
        },
        {
            'title': 'Region Prompting in Adobe Firefly',
            'desc': 'Prompting different regions of an image independently in Firefly, enabling control over the size and orientation of objects. Presented at Adobe MAX 2024.',
            'role': 'Project lead',
            'venue': 'Adobe MAX, 2024',
            'img': 'assets/img/work/region_prompting.jpg',
        },
        {
            'title': 'Grasping Virtual Objects with Real Hands for Extended Reality',
            'desc': "Enabling users to grasp and interact with virtual objects in extended reality using their own hands, just as they would with real objects.",
            'role': 'Inventor',
            'venue': 'Snap Research, US Patent',
            'img': 'assets/img/work/grasp_xr.jpg',
        },
    ]

def get_work_thumbnail(entry):
    if 'video' in entry:
        poster = f' poster="{entry["poster"]}"' if 'poster' in entry else ''
        return f"""<video src="{entry['video']}"{poster} class="work-thumb" autoplay muted loop playsinline></video>"""
    if 'img' in entry:
        return f"""<img src="{entry['img']}" class="work-thumb" alt="{entry['title']}">"""
    return """<div class="work-thumb work-thumb-placeholder">Media coming soon</div>"""

def get_work_entry(entry):
    title = f"""<span class="work-title">{entry['title']}</span>"""

    s = """<div class="row work-entry"><div class="col-sm-4">"""
    s += get_work_thumbnail(entry)
    s += """</div><div class="col-sm-8">"""
    s += f"""{title}<br><span class="work-meta">{entry['role']} &middot; {entry['venue']}</span><br>{entry['desc']}"""
    s += """</div></div>"""
    return s

def get_selected_work_html():
    return "".join(get_work_entry(e) for e in get_selected_work())


def get_news():
    # Newest first. The first NEWS_VISIBLE items are shown; the rest sit behind "Show all".
    return [
        ('Oct 2026', 'We released <a href="https://zero-real.github.io/" target="_blank">ZAP</a>, a robot agent policy trained entirely in simulation.'),
        ('May 2026', 'I joined Luma AI as a Research Scientist.'),
        ('Feb 2024', 'Our work on generating plausible hands in diffusion-based text-to-image models is accepted to CVPR 2024.'),
        ('Feb 2024', 'Our work on segmenting and tracking hand-held objects is accepted to CVPR 2024.'),
        ('Feb 2024', 'I joined Adobe Firefly as a full-time Research Scientist.'),
        ('Feb 2024', 'I successfully defended my PhD. This has been a fantastic journey!'),
        ('Dec 2023', 'I completed a research internship at Adobe Research.'),
        ('Sep 2023', 'Our preliminary work on diffusion-based hand generation is accepted at ICCV 2023 Hands Workshop.'),
        ('Oct 2022', 'I talked about our work on hand analysis at Adobe Research. Thanks <a href="https://research.adobe.com/person/yi-zhou/" target="_blank">Yi Zhou</a> and <a href="https://research.adobe.com/person/yang-zhou/" target="_blank">Yang Zhou</a> for hosting.'),
        ('Sep 2022', 'I completed a research internship at Snap Research, NYC.'),
        ('Jul 2022', 'I gave a talk about our work on hand analysis at the Max Planck Institute for Intelligent Systems. Thanks <a href="https://ps.is.mpg.de/person/sdwivedi" target="_blank">Sai Dwivedi</a>, <a href="https://ps.is.mpg.de/~dtzionas" target="_blank">Dimitrios Tzionas</a>, and <a href="https://ps.is.mpg.de/~black" target="_blank">Michael Black</a> for hosting.'),
        ('Mar 2022', 'Two papers at CVPR 2022: our work on hand-body association and hand tracking.'),
        ('Aug 2021', 'I completed a research internship at Microsoft.'),
        ('Sep 2020', 'Our work on joint hand detection and contact recognition is accepted to NeurIPS 2020.'),
        ('Jul 2019', 'Our work on detecting hands in unconstrained environments is accepted to ICCV 2019.'),
        ('Jul 2019', 'Our work on hand interactions in manual assembly settings is accepted to BMVC 2019.'),
        ('Aug 2018', 'I started my graduate studies at the Department of Computer Science, Stony Brook University.'),
    ]

NEWS_VISIBLE = 2

def get_news_html():
    def items(news):
        return "".join(f"""<li><span class="news-date">{date}</span><span>{text}</span></li>""" for date, text in news)
    news = get_news()
    s = f"""<ul class="news">{items(news[:NEWS_VISIBLE])}</ul>"""
    if len(news) > NEWS_VISIBLE:
        s += f"""<div class="collapse" id="moreNews"><ul class="news">{items(news[NEWS_VISIBLE:])}</ul></div>"""
        s += """<button class="btn btn-link news-toggle" type="button" data-toggle="collapse" data-target="#moreNews" aria-expanded="false" aria-controls="moreNews">Show all news</button>"""
    return s


def get_index_html():
    news = get_news_html()
    work = get_selected_work_html()
    pub = get_publications_html()
    name, headline, bio_text, footer = get_personal_data()
    description = "Research Scientist at Luma AI working on multimodal foundation models for Physical AI, Robotics, and Image &amp; Video Generation."
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css"
    integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap">
  <style>
    :root {{ --bg: #ffffff; --text: #212529; --muted: #6c757d; --link: #0062cc; --surface: #ffffff; --border: #dee2e6; }}
    @media (prefers-color-scheme: dark) {{
      :root {{ --bg: #16181b; --text: #e4e6ea; --muted: #9aa0a6; --link: #7ab4ff; --surface: #22252a; --border: #3a3f45; }}
    }}
    body {{ background: var(--bg); color: var(--text); font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    .display-4 {{ letter-spacing: -0.02em; }}
    a, .btn-link {{ color: var(--link); }}
    .img-thumbnail, .card {{ background: var(--surface); border-color: var(--border); }}
    pre, code {{ color: var(--text); }}
    ul.news {{ list-style: none; padding-left: 0; margin-bottom: 0; line-height: 1.5; }}
    ul.news li {{ display: flex; margin-bottom: 0.4em; }}
    .news-date {{ flex: 0 0 5.5em; color: var(--muted); }}
    .news-toggle {{ padding: 0; margin-top: 0.4em; }}
    .headline {{ text-align: center; font-size: 1.25rem; color: var(--muted); margin-top: 0.25em; }}
    .work-entry {{ margin-bottom: 2em; }}
    .pub-thumb {{ display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border: 1px solid var(--border); border-radius: 6px; }}
    .pub-thumb-contain {{ object-fit: contain; background: #ffffff; padding: 4px; }}
    @media (max-width: 575px) {{ .pub-thumb {{ margin-bottom: 0.75em; }} }}
    .site-footer {{ font-size: 0.85rem; color: var(--muted); }}
    .work-thumb {{ display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border: 1px solid var(--border); border-radius: 6px; background: var(--surface); }}
    .work-thumb-placeholder {{ display: flex; align-items: center; justify-content: center; color: var(--muted); font-size: 0.9rem; }}
    .work-title {{ font-weight: 600; font-size: 1.1rem; }}
    .work-meta {{ color: var(--muted); }}
    @media (max-width: 767px) {{
      .display-4 {{ font-size: 2.25rem; }}
      .profile-photo {{ display: block; max-width: 200px; margin: 0 auto 1em; }}
    }}
    @media (max-width: 575px) {{ .work-thumb {{ margin-bottom: 0.75em; }} }}
  </style>
  <title>{name[0] + ' ' + name[1]}</title>
  <meta name="description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://supreethn.github.io/">
  <meta property="og:title" content="{name[0] + ' ' + name[1]}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="https://supreethn.github.io/assets/img/profile.png">
  <meta name="twitter:card" content="summary">
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
                    <p class="headline">{headline}</p>
                    </div>
                    <br>
                    <div class="col-md-9" style="">
                        {bio_text}
                    </div>
                    <div class="col-md-3" style="">
                        <img src="assets/img/profile.png" class="img-thumbnail profile-photo" width="400px" alt="Profile picture">
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>News</h4>
                        {news}
                    </div>
                </div>
                <div class="row" style="margin-top: 1em;">
                    <div class="col-sm-12" style="">
                        <h4>Selected Work</h4>
                        {work}
                    </div>
                </div>
                <div class="row" style="margin-top: 2em;">
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
        </div>
    </div>

    <!-- jQuery first, then the Bootstrap bundle (includes Popper) -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"
      integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
      crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct"
      crossorigin="anonymous"></script>
    <script>
      $('#moreNews').on('show.bs.collapse', function () {{ $('.news-toggle').text('Show less'); }});
      $('#moreNews').on('hide.bs.collapse', function () {{ $('.news-toggle').text('Show all news'); }});
    </script>
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
