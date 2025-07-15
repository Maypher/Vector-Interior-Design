vcl 4.1;

include "hit-miss.vcl";

backend default {
    .host = "payload";
    .port = "3000";
}

acl purge {
    "localhost";
    "payload";
}

sub vcl_recv {
    // Don't cache admin or api requests (unless it's for media)
    if (req.url  ~ "^\/admin.*$" || req.url ~ "^\/api\/(?!media).*$") {
        return(pass);
    }

    // Pipe websocket to the backend to enable hmr during development 
    if (req.http.upgrade ~ "(?i)websocket") {
        return (pipe);
    }

    if (req.method == "PURGE") {
        if (!client.ip ~ purge) {
            return(synth(405, "Not allowed"));
        }
        return(purge);
    } elseif (req.method == "POST") {
        // Don't cache post requests
        return(pass);
    }

    return(hash);
}

sub vcl_hash {
    // Cache all /_next/ requests
    if (req.url ~ "^\/_next\/?.*$") {
        hash_data(req.http.host);
        hash_data(req.url);
    } else {
        // Replace params for all base urls
       hash_data(regsub(req.url, "\?.*", ""));
    }

    return(lookup);
}

sub vcl_pipe {
    if (req.http.upgrade) {
        set bereq.http.upgrade = req.http.upgrade;
        set bereq.http.connection = req.http.connection;
    }
}