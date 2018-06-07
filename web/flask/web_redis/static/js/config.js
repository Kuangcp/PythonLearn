const app = '/redis/api/v1.0';

function handleGet(url, success, fail) {
    const request = $.get({
        url: app + '' + url,
    });
    request.done(success);
    request.fail(fail);
}

function handlePost(url, data, success, fail) {
    const request = $.post({
        url: app + '' + url,
        contentType: "application/json",
        data: JSON.stringify(data)
    });
    request.done(success);
    request.fail(fail);
}