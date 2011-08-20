**L’art d’art** is a simple django app which uses the yellowapi to find art
galleries next to the user. It displays results using a google map.

This project was created and released as part of Vancouver Hack Days
(http://hackdays.ca).

TODO:

* Add position javascript AJAX for request
* Add request view

KNOWN BUGS:

* Slugs currently undergo a name-collision when being saved. This is because
the unique_slugify function isn't working correctly. This sometimes causes
detailed pages to fail to load.
