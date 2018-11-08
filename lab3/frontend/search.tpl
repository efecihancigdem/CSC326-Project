<!DOCTYPE html>
  <html>

    <head>
      <title>Kajima | Results</title>
    </head>

    <body>
      <img src="/image/kajima" alt="Kajima" usemap="#Logo" style="width:300px;height:150px;">
        <map name="Logo">
        <area shape="rect" coords="0,0,300,150" alt="Kajima" href="http://127.0.0.1:8080/">
        </map>

    </body>
    %if logged_in== True:
      <h1 style="font-size:125%;"> Hi {{user}}, Here is your Research Results by Kajima </h1>
    %else:
      <h2> Research Results by Kajima</h2>
    %end

    <p> You searched: <i>"{{query}}"</i> </p>

    <h1 style="font-size:125%;"> Search Results </h1>
    <table id="results">
      <tr>
        <th>Word</th>
        <th>Count</th>
      </tr>
    %for x in range(len(name)):
      <tr>
        <td>{{name[x]}}</td>
        <td>{{freq[x]}}</td>
      </tr>
    %end
    </table>
    <p>Please click Kajima logo or <a href="http://127.0.0.1:8080/">here</a> to go back to home page </p>

    %if logged_in== True:
      <a href="/signout" class="previous"> Sign out</a>
    %end

    <form action="/" method="get">
    <p>Input your search here: <p> <input name="keywords" type="text" placeholder="Search Here">
    <input type="submit" class = "previous" value="submit">
    </form>

    </body>
  </html>
