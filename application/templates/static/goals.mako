<%include file="../snippets/head.mako" />

<%include file="../snippets/header.mako" />

<div id="goals-page" class="container">
	<%include file="../snippets/page-menu.mako"/>
	<div class="page-intro-section">
	<p>With your help, this dynamic and collaborative Atlas will keep an up-to-date database of all the community innovation spaces, and hopefully encourage more networking and linkages amongst these spaces worldwide. We're making a map and public wiki for anyone to add new spaces and correct information about existing spaces.</p>
			<p>On the back-end, we’re standardizing a set of tags and other datafields and building a data structure (API or Application Programming Interface) in conjunction with Rob Baker’s Maker.json, so all data hosted on this Atlas can be easily shared across other sites. Just as uniformly-sized shipping containers make it easier to ship goods around the world, APIs establish a uniform standard for sharing information around the internet– so anyone can take this open-source Atlas (or some subset of the Atlas) for their own websites and platforms.</p>
			<p>Please keep in mind that there are likely a number of errors in the information about spaces, as we’ve gathered data from a bunch of different databases-- many of which are user-generated and outdated. When you catch mistakes or omissions, kindly let us know.</p>
 	
	</div>
	<section class="page-content">
		<h2 class="section-header dark-blue">What’s a “community innovation space”?</h2>
		<div class="columns two">
			<div>
			<img src="${request.static_url('atlas_of_innovation:static/images/goals.png')}">
			<p class="caption">image of MITERS via Bilal Ghalib</p>
			</div>
			<div>
				<ul class="source-sans">
					<li>A <strong>community</strong> of people eager to collaborate with others— the space must be either open to the public or available for outside partnerships</li>
					<li>Support for old and/or new technological <strong>innovation</strong>, including hardware, software, metal-working, handicrafts, design thinking, repurposed trash, farming, etc.</li>
					<li>A physical or virtual <strong>space</strong> (or temporary event) that promotes creativity and nurtures new ideas</li>
				</ul>
				<div></div>
			</div>
		</div>
	</section>
</div>

<%include file="../snippets/footer.mako" />
