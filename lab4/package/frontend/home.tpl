<!DOCTYPE html>
	<html>
		<head>
			<title>Kajima | Your search engine</title>
			<meta name="viewport" content="width=device-width" >
			
			<style>
			a {
			    text-decoration: none;
			    display: inline-block;
			    padding: 8px 16px;
			}

			a:hover {
			    background-color: #ddd;
			    color: black;
			}

			.previous {
			    background-color: #f1f1f1;
			    color: black;
			}

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
			table#history tr:nth-child(even) {
			    background-color: #eee;
			}
			table#history tr:nth-child(odd) {
			   background-color: #fff;
			}
			table#history th {
			    background-color: black;
			    color: white;
			}
			</style>
		</head>
	<body>
	<img src="/image/kajima" alt="Kajima" usemap="#Logo" style="width:300px;height:150px;">
	<map name="Logo">
	  <area shape="rect" coords="0,0,300,150" alt="Kajima" href="http://100.24.87.175:80/">
	</map>
	</body>
	%if logged_in== True:
		<h2> Welcome to Kajima {{user}}</h2>
	%else:
		<h2> Welcome to Kajima</h2>
	%end
	<form action="/" method="get">
	<p>Input your search here: <p> <input name="keywords" type="text" placeholder="Search Here">
	<input type="submit" class = "previous" value="submit">
	</form>

	%if logged_in== False:
		<a href="/signin" class="previous"> Sign in</a>
	%else:
		<a href="/signout" class="previous"> Sign out</a>
	%end

	%if logged_in== True:
		<h2> Search History </h2>
		<table id="history">
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
	%end
	</table>
	</html>
