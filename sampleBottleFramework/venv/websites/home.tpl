<!DOCTYPE html>
<html>
<head>
<title>Kajima</title>
<style>
table {
}
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 15px;
    text-align: left;
}
table#t01 tr:nth-child(even) {
    background-color: #eee;
}
table#t01 tr:nth-child(odd) {
   background-color: #fff;
}
table#t01 th {
    background-color: black;
    color: white;
}
</style>
</head>

<body>


<img src="/image/kajima" alt="Kajima" usemap="#Logo" style="width:300px;height:150px;">

<!-- Dont forget to change w3schools -->
<map name="Logo">
  <area shape="rect" coords="0,0,300,150" alt="Kajima" href="http://127.0.0.1:8090/">
</map>

</body>

<form action="/login" method="post"> 
Username: <input name="username" type="text" /> 
Password: <input name="username" type="password" /> 
<input value="Login" type="submit" />
 </form>

<form action="/search" method="post">
<p>Input your search here: <p> <input name="search" type="text" >
<input type="submit" value="submit">
</form>

<br>
<br>

<table id="t01">
  <tr>
    <th>Word</th>
    <th>Count</th>
  </tr>
  <tr>
    <td>asdasdad</td>
    <td>asdasda</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
  </tr>
  <tr>
    <td>John</td>
    <td>Doe</td>
  </tr>
</table>



</html>
