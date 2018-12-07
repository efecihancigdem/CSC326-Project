<!DOCTYPE html>
  <html>
    <head>
      <link rel="shortcut icon" type="image/x-icon" href="/img/favicon.ico" />
      <title>Kajima | Results</title>
      <link rel="stylesheet" type="text/css" href="/css/style.css">
      <link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css">
    </head>
    <body>
      <header>
        <div class = "container">
          <div id = "branding">
            <h1> <span class = "highlight" >Kajima </span> Search Engine</h1>
          </div>  
          <nav>
          <ul>
            <li class = "current">
              <a href="http://127.0.0.1:8090/"> Home</a>
            </li>
            <li>
              <a href="http://127.0.0.1:8090/about"> About</a>
            </li>
          </ul>
          </nav>
        </div>
      </header>
      <div class = "mode">
          %if logged_in==0:
            <a href="/signin" class="buttonz">
            Sign-in<br />
            <i class="fab fa-google"></i>
            </a>
          %else:
            <a href="/signout" class="buttonz">Sign Out<br />
            <i class="fab fa-google"></i>
            </a>
          %end
      </div>
      <div class= "container">
        %if logged_in== True:
          <h1 style="font-size:125%;"> Hi {{user}}, Here is your Research Results by Kajima </h1>
        %else:
          <h2> Research Results by Kajima</h2>
        %end
        %if link_num == 0:
            <p> No results found make a new search
            ! </p>
        %else:
            <p> You searched: <i>"{{query}}"</i> </p>

            <div class= "results">
              %if (current_page*6) < len(description):
                %for x in range(((current_page-1)*6),current_page*6):
                  <li>
                    <p>
                      Finding number {{x+1}}
                    </p>
                    <p>
                      {{description[x]}}
                    </p>
                    <a href={{link[x]}} target="_blank"> {{website_name[x]}}</a>
                  </li>
                %end
              %else:
                %for x in range(((current_page-1)*6),len(description)):
                  <li>
                    <p>
                      Finding number {{x+1}}
                    </p>
                    <p>
                      {{description[x]}}
                    </p>
                    <a href={{link[x]}} target="_blank"> {{website_name[x]}}</a>
                  </li>
                %end
              %end
            </div>
            <div class = "clear">
        %end
        </div>
        <br>
        <div class = "bottom_search_bar">
            <p>Please click Home button or <a href="http://127.0.0.1:8090/">here</a> to go back to home page </p>

            %if logged_in== True:
              <a href="/signout" class="previous"> Sign out</a>
            %end

            <form action="/" method="get">
              <input name="keywords" type="text" placeholder="Enlighten Your World">
              <input type="submit" class = "previous" value="Enlighten">
            </form>
        </div>
        % if total_page>1:
          <div class="pagination">
            %if prev_link!= "none":
              <a href={{prev_link}}>&laquo Prev</a>
            %end
            %for x in range(total_page):
              %if current_page == x+1:
                <a class="active" href={{base_link+"&page_no="+str(x+1)}}>{{current_page}}</a>
              %else:
                <a href={{base_link+"&page_no="+str(x+1)}}>{{x+1}}</a>
              %end
            %end
            %if next_link!= "none":
              <a href={{next_link}}>Next &raquo;</a>
            %end
          </div>
        %end
      </div>
      <footer>
        <p> Kajima, Copyright &copy; 2018</p>
      </footer>
    </body>
  </html>
