<!DOCTYPE html>
<%include file="snippets/head.mako" />
<%include file="snippets/header.mako" />
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

<div class="container wiki-content source-sans">
	<div class="columns two columns-wide">
		<div>
			<div id="wiki-list-content">
			<ul class="wiki-list">
			
				</ul>
			</div>
		</div>
		</div>
		</div>
<input type="hidden" name="type" value=${filtertype} id="filter_type" />
<input type="hidden" name="name" value=${filterparam|u} id="filter_name" > 		
<script type='text/javascript' src="/static/js/wikilist.js"></script>
<%include file="snippets/footer.mako" />
