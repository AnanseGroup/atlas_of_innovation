<html>
<head>
  <link href="https://fonts.googleapis.com/css?family=Libre+Baskerville|Source+Sans+Pro:200,300,300i,400,600" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="/static/css/wikipage.css"/>
  <link rel="stylesheet" type="text/css" href="/static/css/stylesheet.css"/>
  <script type='text/javascript' src='/js/wiki.js'></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
</head>
<body>
 <%include file="snippets/header.mako" />
 
 <div class="wBlockHeader">
  <div class="w-top-navigation">
    <a href="/editspace/${primary_id}" >
    	<img src="/static/images/edit_button.png" id="w-top-navigation-bar-edit-button">
    </a>
<!--a href="/" >
    	<img src="/assets/flag_button.png" id="w-top-navigation-bar-flag-incorrect-button">
    </a-->
<!--/div>
 <div class="wnavigation-bar">
    <a href="/" id="wnavigation-bar-article-button" class="navigation-bar-button selected-navigation-bar-button">Article</a>
    <a href="/" id="wnavigation-bar-talk-button" class="navigation-bar-button">Talk</a>
    <a href="/" id="wnavigation-bar-document-revision-button" class="navigation-bar-button">Revision</a>
	</div>
</div-->
<div class="wBlockOne">
  <!-- <img src="/static/images/Placeholder_logo.png" alt="#" style="height: 100px; display:block;margin-left: auto;margin-right: auto;"> -->
  <p ></p>
  <h2 id="wTitle">${name}</h2>
  % if primary_website != None:
  <a id="wWebsite" href="http://${primary_website | n}" target="_blank">${primary_website | n}</a>
  % endif
  % if status != None:
  <p id="wStatus">${status}</p>
  % else:
  <p id="wStatus">Unknown Activity Level</p>
  % endif
  % if types != None:
  <p id="wType">${types}</p>
  % else:
  <p id="wType">Hub</p>
  % endif
  % if description != None:
  <p id="w-space-description">${description}</p>
  % endif
  <hr />
</div>

<div class="wBlockFour">
  <div class="rowAlign">
    <div class="rowTextBlock">
      <p id="wBlockSubTitle">Contact Info</p>
      % if email != None:
      <a href= "mailto:${email | n}">${email | n}</a>  
      % endif
      <br/>
      <div id="w-address">  
       <p><img src="/static/images/pin_map.png" alt="" style="width:8px;height: 10px;">${street_address}</p> 
       % if city != None:
       ${city}, 
       % endif
       % if state != None:
      ${state}, 
       % endif
       % if country != None:
       <a href="/uifunc/wikilist/country?name=${country}">${country}</a>
       % endif
     </div> 
   </div>
   <div class="rowTextBlock">
     <p id="wBlockSubTitle">External Links</p>
     <div class="social-media-block">

       % if twitter != None:
       <a href="${twitter | n}"  id="w-social-button" class="w-social-link">
         <img src="/static/images/social_twitter.png" class="w-social-button" >
       </a>
       % endif
       % if googleplus != None:
       <a href="${googleplus | n}"  id="w-social-gplus"  class="w-social-link">
         <img src="/static/images/social_google+.png" class="w-social-button">
       </a>
       % endif
       % if fablabs_url != None:
       <a href="${fablabs_url | n}" id="w-social-fablab" class="w-social-link">
         <img src="/static/images/social_fablab.png"  class="w-social-button">
       </a>
       % endif
       % if facebook != None:
       <a href="${facebook | n}"  id="w-social-facebook" class="w-social-link">
         <img src="/static/images/social_facebook.png"  class="w-social-button">
       </a>
       %endif
     </div>
   </div>
   % for field, value in generic.items():
      % if not value == None:
         <div class="rowTextBlock">
          <p id="wBlockSubTitle">${field}</p>
          <p id="textBlock">${value}</p>
        </div>
      % endif
  % endfor
</div>

<div class="wBlockTh">
  % if image_url != None:
  <div  class="w-block-center">
   <img src="${image_url}" alt="" style="height: 250px; display:block;margin-left: auto;margin-right: auto;" >   
   
 </div>
</div>
% endif
% if last_updated != None:
<p>${last_updated}</p>
% endif
</body>
</html>