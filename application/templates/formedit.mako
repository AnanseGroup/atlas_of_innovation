<!DOCTYPE html>
<%include file="snippets/head.mako" />

<%include file="snippets/header.mako" />
 <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script type='text/javascript' src="${request.static_url('atlas_of_innovation:static/js/editform.js')}"></script>
<link rel="stylesheet" type="text/css" href="${request.static_url('atlas_of_innovation:static/css/stylesheet.css')}"/>
<link rel="stylesheet" type="text/css" href="${request.static_url('atlas_of_innovation:static/css/form.css')}"/>
<form id="rendered-form" name="editspace" method="get" action="/api/changeSpace/${request.matchdict['id']}">
<fieldset>
<div class="fb-text form-group field-text-name"><label for="text-name" class="fb-text-label">Name <span class="required">*</span> </label> <input type="text" required="" class="form-control" name="name" id="text-name" aria-required="true"></div>
</fieldset>
<fieldset>
<div class="fb-select form-group field-primary-type"><label for="types" class="fb-select-label">Type <span class="required">*</span> </label><select type="select" required="" class="form-control" name="types" id="types" aria-required="true"><option value="Hub">Hub</option><option value="Workshop">Workshop</option><option value="Event">Event</option>
<option value="Gallery">Gallery</option>
<option value="Retail">Retail</option>
<option value="Virtual">Virtual</option>
<option value="Cluster">Cluster</option>
<option value="Ecovillage">Ecovillage</option>
</select></div>
<fieldset>
<fieldset>
<div class="fb-undefined form-group field-textarea-address"><label for="textarea-address" class="fb-textarea-label">Street Address  </label><textarea rows="4" type="textarea" class="form-control" name="street_address" id="textarea-address"></textarea></div>
</fieldset>
<fieldset>
<div class="fb-text form-group field-text-city"><label for="text-city" class="fb-text-label">City </label> <input type="text"  class="form-control" name="city" id="text-city" ></div>
</fieldset>
<fieldset>
<div class="fb-text form-group field-text-country"><label for="text-country" class="fb-text-label">Country <span class="required">*</span> </label> <input type="text" required="" class="form-control" name="country" id="text-country" aria-required="true"></div>
</fieldset>
<fieldset>
<div class="fb-email form-group field-text-email"><label for="text-email" class="fb-email-label">Email </label> <input type="text"  class="form-control" name="email" id="text-email" ></div>
</fieldset>
<fieldset>
<div class="fb-undefined form-group field-textarea-description"><label for="textarea-description" class="fb-textarea-label">Description  </label><textarea rows="4" type="textarea" class="form-control" name="description" id="textarea-description"></textarea></div>
</fieldset>
<fieldset>
<div class="fb-number form-group field-number-phone"><label for="number-phone" class="fb-number-label">Phone Number  </label> <input type="text" class="form-control" name="phone" id="number-phone"></div>
</fieldset>
<fieldset>
<div class="fb-select form-group field-them"><label for="theme" class="fb-select-label">Theme <span class="required">*</span> </label><select type="select" required="" class="form-control" name="theme" id="theme" aria-required="true">
<option value="Agriculture">Agriculture</option>
<option value="Appropriate Technology">Appropriate Technology</option>
<option value="Biology">Biology</option>
<option value="Design">Design</option>
<option value="Education">Education</option>
<option value="Food">Food</option>
<option value="Materials">Materials</option>
<option value="Media">Media</option>
<option value="Politics">Politics</option>
<option value="Science">Science</option>
<option value="Youth">Youth</option>
</select></div>
<fieldset>
<fieldset> 
<br/>
<div class="fb-checkbox form-group field-checkbox-services"><label for="checkbox-services" class="fb-checkbox-group-label">Services  </label><br/><div class="checkbox-group"><input value="Coworking" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-0" > <label for="checkbox-services-0">Coworking</label><br><input value="Making" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-1"> <label for="checkbox-services-1">Making</label><br><input value="Hosting events" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-2"> <label for="checkbox-services-2">Hosting Events</label><br><input value="Selling" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-3" ><label for="checkbox-services-3">Selling</label><br><input value="Trading" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-4" ><label for="checkbox-services-4">Trading</label><br>
<input value="Incubating Startup" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-5" > <label for="checkbox-services-5">Incubating Startup</label><br>
<input value="Educating" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-6" > <label for="checkbox-services-6">Educating</label><br>
<input value="Vocational training" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-7" > <label for="checkbox-services-7">Vocational training</label><br>
<input value="Investing" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-8" > <label for="checkbox-services-8">Investing</label><br>
<input value="Mentoring" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-9" > <label for="checkbox-services-9">Mentoring</label><br>
<input value="Donating" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-10" > <label for="checkbox-services-10">Donating</label><br>
<input value="Transferring technology" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-11" > <label for="checkbox-services-11">Transferring technology</label><br>
<input value="Coliving" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-12" > <label for="checkbox-services-12">Coliving</label><br>
<input value="Repairing" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-13" > <label for="checkbox-services-13">Repairing</label><br>
<input value="Manufacturing" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-14" > <label for="checkbox-services-14">Manufacturing</label><br>
<input value="Prototyping" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-15" > <label for="checkbox-services-15">Prototyping</label><br>
<input value="Researching" type="checkbox" class="checkbox-group" name="services" id="checkbox-services-16" > <label for="checkbox-services-16">Researching</label><br>
</div></div>
</fieldset>
<div class="fb-select form-group field-select-status"><label for="select-status" class="fb-select-label">Status </label><select type="select"  class="form-control" name="status" id="select-status" ><option value="unknown" selected="true">Unknown</option> <option value="Active" selected="true">Active</option><option value="inactive">Inactive</option><option value="planned">Planned </option></select></div>
<fieldset>
<div class="fb-undefined form-group field-textarea-tools"><label for="textarea-tools" class="fb-textarea-label">Capabilities  </label><textarea type="textarea" class="form-control" name="tools" id="textarea-tools"></textarea></div>
</fieldset>
<fieldset>
<div class="fb-select form-group field-primary-type"><label for="members" class="fb-select-label">Members</label><select type="select" class="form-control" name="number_of_members" id="members" >
<option value="Unknown"> Unknown</option>
<option value="1 to 50">1 to 50</option>
<option value="51 to 100">51 to 100</option>
<option value="101 to 500">101 to 500</option>
<option value="500+">500+</option>
</select></div>
</fieldset>
<fieldset>
<div class="fb-select form-group field-primary-type"><label for="affiliation" class="fb-select-label">Affiliations </label><select type="select"  class="form-control" name="network_affiliation" id="affiliation" >
<option value="Hackerspaces"> Hackerspaces.org</option>
<option value="Fab Labs">Fablabs</option>
<option value="Impact Hub">Impact Hub</option>
<option value="Afri Lab">Afri Lab</option>
<option value="GlobalEcovillage">Global Eco Village Network</option>
<option value="Hackerbases"> Hackerbases</option>
<option value="Maker Faire">Maker Faire</option>
<option value="RepairCafe">RepairCafe</option>
<option value="Tech Shop">Tech Shop</option>
<option value="Global Innovation Gathering"> Global Innovation Gathering</option>
<option value="Other">Other</option>
</select></div>
</fieldset>
<fieldset>
<div class="fb-checkbox form-group field-checkbox-services"><label for="checkbox-services" class="fb-checkbox-group-label">Ownership  </label><br/><div class="checkbox-group"><input value="Civil Society" type="checkbox" class="checkbox-group" name="ownership" id="checkbox-ownership-0" > <label for="checkbox-ownership-0">Civil Society</label><br><input value="Private Sector" type="checkbox" class="checkbox-group" name="ownership" id="checkbox-ownership-1"> <label for="checkbox-ownership-1">Private Sector</label><br><input value="Hybrid Led" type="checkbox" class="checkbox-group" name="ownership" id="checkbox-ownership-2"> <label for="checkbox-ownership-2">Hybrid Led</label><br><input value="Government" type="checkbox" class="checkbox-group" name="ownership" id="checkbox-ownership-3" ><label for="checkbox-ownership-3">Government</label><br><input value="Academic" type="checkbox" class="checkbox-group" name="ownership" id="checkbox-ownership-4" ><label for="checkbox-ownership-4">Academic</label><br><input value="University" type="checkbox" class="checkbox-group" name="ownership" id="checkbox-ownership-5" > <label for="checkbox-ownership-5">University</label><br>
</div></div>
<br/>
</fieldset>
 <button type="cancel" id="space-cancel" onclick="window.location='/wikipage/${request.matchdict['id']}';return false;">Cancel</button>
 <button type="submit" id="space-submit">Submit</button>
</form>
<%include file="snippets/footer.mako" />
