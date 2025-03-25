local _M = {}

local ngx = require("ngx")
local lrucache = require "resty.lrucache"
local ngx_pipe = require "ngx.pipe"

local c, err = lrucache.new(200) -- allow up to 200 items in the cache
if not c then
    error("failed to create the cache: " .. (err or "unknown"))
end

function _M.watermark_image()
    local image_filename = ngx.var.uri:match("([^/]+)$")
    local img_path = "/storage/images/" .. image_filename

    local cached_image = c:get(image_filename)

    if cached_image then
        ngx.log(ngx.INFO, "SERVING FROM CACHE")
        ngx.header.content_type = 'image/webp'
        ngx.say(cached_image)
        return ngx.exit(ngx.HTTP_OK)
    end

    ngx.log(ngx.INFO, "GENERATING IMAGE")

    local cmd = string.format(
        'magick %s -quality 75 webp:-',
        img_path)


    local proc, error = ngx_pipe.spawn(cmd)

    if not proc then
        ngx.log(ngx.ERR, "failed to spawn command: ", error)
        return ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
    end

    local output, output_err = proc:stdout_read_all()
    local error_data, error_error = proc:stderr_read_all()

    if not output then
        ngx.log(ngx.ERR, "failed to read output: ", output_err)
        return ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
    end

    if error_data and error_data ~= '' then
        ngx.log(ngx.ERR, "image transformation error: ", error_data)
        return ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
    end

    c:set(image_filename, output, 2)

    ngx.header.content_type = 'image/webp'
    ngx.say(output)
    return ngx.exit(ngx.HTTP_OK)
end

return _M
