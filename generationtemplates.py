
LIST_GENERATION_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <h1>Generations</h1>
    <hr>
    %s
    <hr>
    <table>
    <tr>
    <td>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
    </td>
    <td>
    <form action="/addgeneration" method="get">
      <div><input type="submit" value="Add"></div>
    </form>
    </td>
    </tr>
    </div>
"""


ADD_GENERATION_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <form action="/doaddgeneration" method="post">
      <div><textarea name="generationname"    rows="1" cols="40"></textarea></div>
      <div><textarea name="generationscript"  rows="1" cols="40"></textarea></div>
      <div><textarea name="generationniter"   rows="1" cols="40"></textarea></div>
      <div><input type="submit" value="Add"></div>
    </form>
    <hr>
    <form action="/" method="get">
      <div><input type="submit" value="Home"></div>
    </form>
"""


VIEW_GENERATION_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <div class="chichar">%s</div>
    <div class="pronunciation">%s</div>
    <div class="translation">%s</div>
    <div class="space"></div>
    <table>
    <tr>
    <td>
    <form action="/editchichar/%s" method="get">
       <div class="charaction"><input type="submit" value="Edit"></div>
    </form>
    </td>
    <td>
    <form action="/strokechichar/%s" method="get">
       <div class="charaction"><input type="submit" value="Stroke"></div>
    </form>
    </td>
    <td>
    <form action="/deletechichar/%s" method="post">
      <div class="charaction"><input type="submit" value="Delete"></div>
    </form>
    </td>
    <td>
    <form action="/addchichar" method="get">
      <div class="charaction"><input type="submit" value="New"></div>
    </form>
    </td>
    <td>
    <form action="/listchichars" method="get">
      <div><input type="submit" value="List"></div>
    </form>
    </td>
    <td>
    <form action="/chicharsentences/%s" method="get">
      <div><input type="submit" value="Sentences"></div>
    </form>
    </td>
    <td>
    <form action="/" method="get">
      <div class="home"><input type="submit" value="Home"></div>
    </form>
    </td>
    </tr>
    </table>
    </div>
"""



EDIT_GENERATION_TEMPLATE = """\
<head>
  <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
    <div align="center">
    <form action="/savechichar/%s" method="post">
       <div><textarea class="chichar" name="chichar"        rows="1" cols="2">%s</textarea></div>
       <div><textarea name="pronunciation"    rows="1" cols="10">%s</textarea></div>
       <div><textarea name="translation"  rows="1" cols="10">%s</textarea></div>
       <div class="space"></div>
       <div id="buttons">
           <table>
           <tr>
           <td>
           <div><input type="submit" name="save" value="Save"></div>
           </td>
           <td>
           <div><input type="submit" name="cancel" value="Cancel"></div>
           </td>
           </tr>
           </table>
           <div style="clear:both"></div>
       </div>
    </form>
    </div>
"""
