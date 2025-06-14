<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8" />
<meta name="generator" content="pandoc" />
<meta http-equiv="X-UA-Compatible" content="IE=EDGE" />




<title>MIPLIB 2017 – The Mixed Integer Programming Library</title>

<script src="site_libs/header-attrs-2.29/header-attrs.js"></script>
<script src="site_libs/jquery-3.6.1/jquery-3.6.1.min.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link href="site_libs/bootstrap-3.3.5/css/cosmo.min.css" rel="stylesheet" />
<script src="site_libs/bootstrap-3.3.5/js/bootstrap.min.js"></script>
<script src="site_libs/bootstrap-3.3.5/shim/html5shiv.min.js"></script>
<script src="site_libs/bootstrap-3.3.5/shim/respond.min.js"></script>
<style>h1 {font-size: 34px;}
       h1.title {font-size: 38px;}
       h2 {font-size: 30px;}
       h3 {font-size: 24px;}
       h4 {font-size: 18px;}
       h5 {font-size: 16px;}
       h6 {font-size: 12px;}
       code {color: inherit; background-color: rgba(0, 0, 0, 0.04);}
       pre:not([class]) { background-color: white }</style>
<script src="site_libs/navigation-1.1/tabsets.js"></script>
<link href="site_libs/highlightjs-9.12.0/textmate.css" rel="stylesheet" />
<script src="site_libs/highlightjs-9.12.0/highlight.js"></script>
<script src="site_libs/kePrint-0.0.1/kePrint.js"></script>
<link href="site_libs/lightable-0.0.1/lightable.css" rel="stylesheet" />

<style type="text/css">
  code{white-space: pre-wrap;}
  span.smallcaps{font-variant: small-caps;}
  span.underline{text-decoration: underline;}
  div.column{display: inline-block; vertical-align: top; width: 50%;}
  div.hanging-indent{margin-left: 1.5em; text-indent: -1.5em;}
  ul.task-list{list-style: none;}
    </style>

<style type="text/css">code{white-space: pre;}</style>
<script type="text/javascript">
if (window.hljs) {
  hljs.configure({languages: []});
  hljs.initHighlightingOnLoad();
  if (document.readyState && document.readyState === "complete") {
    window.setTimeout(function() { hljs.initHighlighting(); }, 0);
  }
}
</script>






<link rel="stylesheet" href="miplib.css" type="text/css" />



<style type = "text/css">
.main-container {
  max-width: 940px;
  margin-left: auto;
  margin-right: auto;
}
img {
  max-width:100%;
}
.tabbed-pane {
  padding-top: 12px;
}
.html-widget {
  margin-bottom: 20px;
}
button.code-folding-btn:focus {
  outline: none;
}
summary {
  display: list-item;
}
details > summary > p:only-child {
  display: inline;
}
pre code {
  padding: 0;
}
</style>


<style type="text/css">
.dropdown-submenu {
  position: relative;
}
.dropdown-submenu>.dropdown-menu {
  top: 0;
  left: 100%;
  margin-top: -6px;
  margin-left: -1px;
  border-radius: 0 6px 6px 6px;
}
.dropdown-submenu:hover>.dropdown-menu {
  display: block;
}
.dropdown-submenu>a:after {
  display: block;
  content: " ";
  float: right;
  width: 0;
  height: 0;
  border-color: transparent;
  border-style: solid;
  border-width: 5px 0 5px 5px;
  border-left-color: #cccccc;
  margin-top: 5px;
  margin-right: -10px;
}
.dropdown-submenu:hover>a:after {
  border-left-color: #adb5bd;
}
.dropdown-submenu.pull-left {
  float: none;
}
.dropdown-submenu.pull-left>.dropdown-menu {
  left: -100%;
  margin-left: 10px;
  border-radius: 6px 0 6px 6px;
}
</style>

<script type="text/javascript">
// manage active state of menu based on current page
$(document).ready(function () {
  // active menu anchor
  href = window.location.pathname
  href = href.substr(href.lastIndexOf('/') + 1)
  if (href === "")
    href = "index.html";
  var menuAnchor = $('a[href="' + href + '"]');

  // mark the anchor link active (and if it's in a dropdown, also mark that active)
  var dropdown = menuAnchor.closest('li.dropdown');
  if (window.bootstrap) { // Bootstrap 4+
    menuAnchor.addClass('active');
    dropdown.find('> .dropdown-toggle').addClass('active');
  } else { // Bootstrap 3
    menuAnchor.parent().addClass('active');
    dropdown.addClass('active');
  }

  // Navbar adjustments
  var navHeight = $(".navbar").first().height() + 15;
  var style = document.createElement('style');
  var pt = "padding-top: " + navHeight + "px; ";
  var mt = "margin-top: -" + navHeight + "px; ";
  var css = "";
  // offset scroll position for anchor links (for fixed navbar)
  for (var i = 1; i <= 6; i++) {
    css += ".section h" + i + "{ " + pt + mt + "}\n";
  }
  style.innerHTML = "body {" + pt + "padding-bottom: 40px; }\n" + css;
  document.head.appendChild(style);
});
</script>

<!-- tabsets -->

<style type="text/css">
.tabset-dropdown > .nav-tabs {
  display: inline-table;
  max-height: 500px;
  min-height: 44px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.tabset-dropdown > .nav-tabs > li.active:before, .tabset-dropdown > .nav-tabs.nav-tabs-open:before {
  content: "\e259";
  font-family: 'Glyphicons Halflings';
  display: inline-block;
  padding: 10px;
  border-right: 1px solid #ddd;
}

.tabset-dropdown > .nav-tabs.nav-tabs-open > li.active:before {
  content: "\e258";
  font-family: 'Glyphicons Halflings';
  border: none;
}

.tabset-dropdown > .nav-tabs > li.active {
  display: block;
}

.tabset-dropdown > .nav-tabs > li > a,
.tabset-dropdown > .nav-tabs > li > a:focus,
.tabset-dropdown > .nav-tabs > li > a:hover {
  border: none;
  display: inline-block;
  border-radius: 4px;
  background-color: transparent;
}

.tabset-dropdown > .nav-tabs.nav-tabs-open > li {
  display: block;
  float: none;
}

.tabset-dropdown > .nav-tabs > li {
  display: none;
}
</style>

<!-- code folding -->




</head>

<body>


<div class="container-fluid main-container">




<div class="navbar navbar-default  navbar-fixed-top" role="navigation">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-bs-toggle="collapse" data-target="#navbar" data-bs-target="#navbar">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="index.html">MIPLIB 2017</a>
    </div>
    <div id="navbar" class="navbar-collapse collapse">
      <ul class="nav navbar-nav">
        <li class="dropdown">
  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
    About
     
    <span class="caret"></span>
  </a>
  <ul class="dropdown-menu" role="menu">
    <li>
      <a href="history.html">History</a>
    </li>
    <li>
      <a href="news.html">News Log</a>
    </li>
    <li>
      <a href="CHANGELOG.html">Changelog</a>
    </li>
    <li>
      <a href="links.html">Links</a>
    </li>
    <li>
      <a href="involved_people.html">Involved People</a>
    </li>
  </ul>
</li>
<li>
  <a href="tag_benchmark.html">Benchmark</a>
</li>
<li>
  <a href="tag_collection.html">Collection</a>
</li>
<li>
  <a href="download.html">Download</a>
</li>
<li class="dropdown">
  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
    Help
     
    <span class="caret"></span>
  </a>
  <ul class="dropdown-menu" role="menu">
    <li>
      <a href="Selection_Methodology.html">Selection Methodology</a>
    </li>
    <li>
      <a href="statistics.html">Instance Statistics Guide</a>
    </li>
  </ul>
</li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        
      </ul>
    </div><!--/.nav-collapse -->
  </div><!--/.container -->
</div><!--/.navbar -->

<div id="header">



<h1 class="title toc-ignore">MIPLIB 2017 – The Mixed Integer Programming
Library</h1>

</div>


<p><a target="_blank" href="wordcloud.html">
<img src="wordcloud4.png" style="height:400px;margin-left:5px;float:right;" alt="Word cloud based on frequencies in instance descriptions"/>
</a> In response to the needs of researchers for access to real-world
mixed integer programs, Robert E. Bixby, E.A. Boyd, and R.R. Indovina
created in 1992 the MIPLIB, an electronically available library of both
pure and mixed integer programs. Since its introduction, MIPLIB has
become a standard test set used to compare the performance of mixed
integer optimizers. Its availability has provided an important stimulus
for researchers in this very active area. The library has now been
released in its sixth edition as a collaborative effort between Arizona
State University, COIN-OR, CPLEX, FICO, Gurobi, MathWorks, MIPCL, MOSEK,
NUOPT, SAS, and Zuse Institute Berlin. Like the previous MIPLIB 2010,
two main sets have been compiled from the submissions. The <a
href="tag_benchmark.html"><strong>Benchmark Set</strong></a> contains
240 instances that are solvable by (the union of) today’s codes. For
practical reasons, the benchmark instances were selected subject to
various constraints regarding solvability and numerical stability. The
much larger <a href="tag_collection.html"><strong>Collection
Set</strong></a> represents a diverse selection regardless of the above,
benchmark-relevant criteria. Download the instance sets as well as
supplementary data, run scripts and the solution checker from our <a
href="download.html">Download page</a>.</p>
<div id="contact-us" class="section level2">
<h2>Contact Us</h2>
<p>The current maintainers of the website and its content are <a
href="https://www.zib.de/gleixner">Ambros Gleixner</a> and <a
href="https://www.zib.de/de/members/turner">Mark Turner</a>.
Contributions of new solutions to open instances are always welcome, and
will be made available in periodic updates of the web page. Also, we are
happy to provide additional instance tags upon request.</p>
<p><strong>Please send your submissions to <a
href="mailto:miplibsolutions@zib.de">miplibsolutions@zib.de</a></strong></p>
</div>
<div id="miplib-2010" class="section level2">
<h2>MIPLIB 2010</h2>
<p>This page now hosts the new MIPLIB 2017. Find its predecessor MIPLIB
2010 on our <a href="links.html">Links</a> page.</p>
</div>
<div id="news-status" class="section level2">
<h2>News &amp; Status</h2>
<div class="row">
<div id="news" class="section level3 col-md-6">
<h3>News</h3>
<table class="table table-striped table-hover" style="margin-left: auto; margin-right: auto;">
<tbody>
<tr>
<td style="text-align:right;">
Mar 07, 2025
</td>
<td style="text-align:left;">
Release of solufile 35 with 1 better incumbents, and 1 instance updated
from hard to easy.
</td>
</tr>
<tr>
<td style="text-align:right;">
Jan 20, 2025
</td>
<td style="text-align:left;">
Release of solufile 34 with 8 better incumbents, and 4 instance updated
from open to hard.
</td>
</tr>
<tr>
<td style="text-align:right;">
Nov 14, 2024
</td>
<td style="text-align:left;">
Release of solufile 33 with 15 better incumbents, and 1 instance updated
from open to easy.
</td>
</tr>
<tr>
<td style="text-align:right;">
Oct 07, 2024
</td>
<td style="text-align:left;">
Release of solufile 32 with 28 better incumbents, 1 instance updated
from open to hard, and 1 instance updated from hard to easy.
</td>
</tr>
<tr>
<td style="text-align:right;">
Jul 18, 2024
</td>
<td style="text-align:left;">
Release of solufile 31 with 22 better incumbents, 1 instance updated
from open to hard, 1 instance updated from open to easy, and 1 instance
corrected from hard to open.
</td>
</tr>
</tbody>
</table>
<p>For all news, click <a href="news.html">here</a>, or view the
complete <a href="CHANGELOG.html">Changelog</a>.</p>
</div>
<div id="status" class="section level3 col-md-6">
<h3>Status</h3>
<div class="figure" style="text-align: center">
<img src="index_files/figure-html/statusplot-1.png" alt="Frequencies of categories easy/hard/open" width="100%" />
<p class="caption">
Frequencies of categories easy/hard/open
</p>
</div>
<p>‘Easy’ means that the instance could be solved within less than one
hour and with at most 16 threads, using an out-of-the-box solver on
standard desktop computing hardware, ‘hard’ stands for instances, that
have been solved in longer runs possibly using nonstandard hardware
and/or algorithms, whereas ‘open’ means, that the instance has not yet
been reported solved.</p>
</div>
</div>
</div>
<div id="citation" class="section level2">
<h2>Citation</h2>
<p>An article about the selection methodology has been published in
Mathematical Programming Computation. Please cite MIPLIB 2017 as
follows:</p>
<pre><code>@article{
  author                   = {Gleixner, Ambros and Hendel, Gregor and Gamrath, Gerald and Achterberg, Tobias and Bastubbe, Michael and Berthold, Timo and Christophel, Philipp M. and Jarck, Kati and Koch, Thorsten and Linderoth, Jeff and L\&quot;ubbecke, Marco and Mittelmann, Hans D. and Ozyurt, Derya and Ralphs, Ted K. and Salvagnin, Domenico and Shinano, Yuji},
  title                    = {{MIPLIB 2017: Data-Driven Compilation of the 6th Mixed-Integer Programming Library}},
  journal                  = {Mathematical Programming Computation},
  year                     = {2021},
  doi                      = {10.1007/s12532-020-00194-3},
  url                      = {https://doi.org/10.1007/s12532-020-00194-3}
}</code></pre>
</div>
<div id="disclaimer" class="section level2">
<h2>Disclaimer</h2>
<p>Most of the data files on this site have been converted, some optimal
solutions are gathered from papers and some data was typed in by hand or
generated by automatic solution extraction programs. While we took every
effort to make no mistakes, we cannot guarantee that everything is
correct. If you find any errors or have doubts about a solution, please
contact us.</p>
</div>

<hr /><address>Last Update 2025 by <a href="https://www.zib.de/de/members/turner">Mark Turner</a>
<br /> generated with <a href="https://rmarkdown.rstudio.com/index.html">R Markdown</a>
<br />&copy;  by Zuse Institute Berlin (ZIB)<br />
<a href="https://www.zib.de/impressum_datenschutz">Imprint</a> </address>
<!-- Piwik -->
<script type="text/javascript">
  var _paq = _paq || [];
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u=(("https:" == document.location.protocol) ? "https" : "http") + "://stat.kobv.de/piwik/";
    _paq.push(['setTrackerUrl', u+'piwik.php']);
    _paq.push(['setSiteId', 39]);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0]; g.type='text/javascript';
    g.defer=true; g.async=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<noscript><p><img src="https://stat.kobv.de/piwik/piwik.php?idsite=39" style="border:0;" alt="" /></p></noscript>
<!-- End Piwik Code -->



</div>

<script>

// add bootstrap table styles to pandoc tables
function bootstrapStylePandocTables() {
  $('tr.odd').parent('tbody').parent('table').addClass('table table-condensed');
}
$(document).ready(function () {
  bootstrapStylePandocTables();
});


</script>

<!-- tabsets -->

<script>
$(document).ready(function () {
  window.buildTabsets("TOC");
});

$(document).ready(function () {
  $('.tabset-dropdown > .nav-tabs > li').click(function () {
    $(this).parent().toggleClass('nav-tabs-open');
  });
});
</script>

<!-- code folding -->


<!-- dynamically load mathjax for compatibility with self-contained -->
<script>
  (function () {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src  = "https://mathjax.rstudio.com/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML";
    document.getElementsByTagName("head")[0].appendChild(script);
  })();
</script>

</body>
</html>
