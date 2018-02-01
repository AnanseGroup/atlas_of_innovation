<%! import random %>

<%include file="snippets/head.mako" />
<%include file="snippets/header.mako" />

<div class="container wiki-content source-sans">
	<div class="columns two columns-wide">
		<!--div>
			<div class="column-content">
				<div class="column-header">
					<h3>Recently Updated</h3>
				</div>
			</div>
		</div-->
		<div>
			<div class="column-content">
				<div class="column-header">
					<h3>Countries</h3>
					<a href="#_" class="see-all">See All</a>
				</div>
				<ul class="wiki-list">
					% for country in countries:
						<a href="/uifunc/wikilist/country/${country}"<li>${country}<!--span class="count pink">(${random.randrange(1,100)})</span--></li></a> <br/>
					% endfor
				</ul>
			</div>
		</div>
		<!--div>
			<div class="column-content">
				<div class="column-header">
					<h3>Services</h3>
					<a href="#_" class="see-all">See All</a>
				</div>
				<ul class="wiki-list">
					% for service in ("Coworking", "Hosting", "Events", "Selling and trading", "Incubating", "Startups", "Educating", "Vocational training", "Mentoring", "Donating", "Transferring", "Technology", "Co-living", "Repairing", "Manufacturing"):
						<li>${service} <span class="count pink">(${random.randrange(1,350)})</span></li>
					% endfor
				</ul>
			</div>
		</div-->
		<div>
			<div class="column-content">
				<div class="column-header">
					<h3>Themes</h3>
					<a href="#_" class="see-all">See All</a>
				</div>
				<ul class="wiki-list">
				% for service in ("Agriculture","Appropriate Technology","Biology","Design","Education","Food","Materials","Media","Politics","Science","Youth"):
	
				<a href="/uifunc/wikilist/theme/${service}"><li>${service}<!--span class="count pink">(${random.randrange(1,350)})</span--></li>
					% endfor
				</ul>
			</div>
		</div>
	</div>
</div>
<script type='text/javascript' src="static/js/wiki.js"></script>

<%include file="snippets/footer.mako" />
