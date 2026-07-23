#!/usr/bin/env lua5.4

-- Port of tpd-21/chat/chat-02.lua to freechains.vcs (single root).

local BASE = '../.freechains'
local ROOT = BASE .. '/root'
local KEYS = BASE .. '/keys'

os.execute("rm -rf " .. BASE)
os.execute("mkdir -p " .. KEYS)

local USERS = {}

function exec (cmd)
    local f = io.popen(cmd .. " 2>&1")
    local v = f:read('*a')
    f:close()
    return (string.gsub(v, "%s+$", ""))
end

function keys (user)
    if not USERS[user] then
        os.execute("ssh-keygen -t ed25519 -N '' -C '' -f " .. KEYS .. "/" .. user .. " -q")
        USERS[user] = {
            user  = user,
            pub   = exec("cat " .. KEYS .. "/" .. user .. ".pub"),
            n     = 0,
            likes = 0,
        }
    end
    return USERS[user]
end

-- the pioneer creates the chain and thus holds the initial reps
keys('Ashlee')
print(exec("freechains --root=" .. ROOT .. " --now=0 chains add '#chat' init inline --sign=" .. KEYS .. "/Ashlee"))

local N = 0
for l in io.lines('wikimedia.chat') do
    l = string.gsub(l, "'", " ")
    local y,m,d,hh,mm,ss,user,msg = string.match(l, "(%d%d%d%d)(%d%d)(%d%d) %[(%d%d):(%d%d):(%d%d)%] %<([%a%d-_]+)%>\t(.*)")
    if y then
        local ts = os.time({ year=y, month=m, day=d, hour=hh, min=mm, sec=ss })
        local t  = keys(user)
        t.n = t.n + 1

        -- query reps at the same virtual time as the post
        local reps = tonumber(exec("freechains --root=" .. ROOT .. " --now=" .. ts .. " chain '#chat' reps author \"" .. t.pub .. "\""))
        local beg  = (reps <= 0) and ' --beg' or ''

        local hash = exec("freechains --root=" .. ROOT .. " --now=" .. ts .. " chain '#chat' post inline '" .. msg .. "'" .. beg .. " --sign=" .. KEYS .. "/" .. user)
        assert(string.match(hash, '^%x+$'), user .. ' : ' .. hash)

        -- welcoming like from the pioneer unblocks a begging post
        if beg ~= '' then
            local v = exec("freechains --root=" .. ROOT .. " --now=" .. ts .. " chain '#chat' like 1 post " .. hash .. " --sign=" .. KEYS .. "/Ashlee")
            assert(string.match(v, '^%x+$'), user .. ' : like : ' .. v)
            t.likes = t.likes + 1
        end

        print(N, ts, user, reps, hash)
    end
    N = N + 1
    if N == 30 then
        break
    end
end

local T = {}
local ns, nlikes = 0, 0
for _,t in pairs(USERS) do
    T[#T+1] = t
end
table.sort(T, function (t1,t2) return t1.likes > t2.likes end)
for _,t in ipairs(T) do
    ns     = ns + t.n
    nlikes = nlikes + t.likes
    print(string.format("%12s", string.sub(t.user,1,12)), t.likes, t.n)
end
print(#T, 'users', '|', (nlikes-#T)/(ns-#T), 'pct', '|', 'n/lk', ns, nlikes)
