local _M = {}

local ngx = require("ngx")
local lrucache = require "resty.lrucache"
local ngx_pipe = require("ngx.pipe")

local c, err = lrucache.new(200) -- allow up to 200 items in the cache
if not c then
    error("failed to create the cache: " .. (err or "unknown"))
end

local function image_exists(path)
    local file = io.open(path, "r")

    if file ~= nil then
        file:close()
        return true
    else
        return false
    end
end

function _M.optimize_image()
    local image_filename = ngx.var.image_filename
    local img_path = "/storage/images/" .. image_filename

    local cached_image = c:get(image_filename)

    if cached_image ~= nil then
        ngx.log(ngx.ERR, "SERVING IMAGE FROM CACHE: ", image_filename)

        local etag = ngx.md5(cached_image)

        -- Check if the client sent If-None-Match header
        local if_none_match = ngx.req.get_headers()["if-none-match"]
        if if_none_match and if_none_match == etag then
            -- Content hasn't changed, return 304 Not Modified
            return ngx.exit(ngx.HTTP_NOT_MODIFIED)
        end

        -- Send cached image with proper headers
        ngx.header.content_type = 'image/webp'
        ngx.header.cache_control = "public, max-age=3600"
        ngx.header.etag = etag

        ngx.header.content_type = 'image/webp'
        ngx.header.cache_control = "max-age=3600"
        ngx.header.expires = ngx.http_time(ngx.time() + 3600)
        ngx.print(cached_image)
        return ngx.exit(ngx.HTTP_OK)
    end

    local img_exists_thread = ngx.thread.spawn(image_exists, img_path)

    local _, img_exists = ngx.thread.wait(img_exists_thread)

    if img_exists then
        ngx.log(ngx.ERR, "GENERATING IMAGE")

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
            ngx.log(ngx.ERR, "image transformation error: ", error_error)
            return ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
        end

        c:set(image_filename, output, 30)

        ngx.header.content_type = 'image/webp'
        ngx.header.cache_control = "public, max-age=3600, immutable"
        ngx.header.expires = ngx.http_time(ngx.time() + 3600)
        ngx.print(output)
        return ngx.exit(ngx.HTTP_OK)
    else
        ngx.exit(ngx.HTTP_NOT_FOUND)
    end
end

return _M
