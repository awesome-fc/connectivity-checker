This is a tool to check the connectivity between a function and other network endpoint, such as website, database, ecs host etc. It's especially useful when the service/function has VPC config. 

After deployment, this tool creates two functions, one is an event function and the other one is a http function. You can use either one to check the connectivity. Since the http function allows annoymous access and anyone knows the http endpoint can access it, you might want to remove it from the template.yml.

## Usage

1. Deploy the tool with funcraft
```
$ fun deploy -y
using region: cn-hangzhou
using accountId: ***********3637
using accessKeyId: ***********FPbL
using timeout: 300

Collecting your services information, in order to caculate devlopment changes...

Resources Changes(Beta version! Only FC resources changes will be displayed):

┌──────────────────────┬──────────────────────────────┬────────┬─────────────┐
│ Resource             │ ResourceType                 │ Action │ Property    │
├──────────────────────┼──────────────────────────────┼────────┼─────────────┤
│ connectivity-checker │ Aliyun::Serverless::Service  │ Modify │ Description │
├──────────────────────┼──────────────────────────────┼────────┼─────────────┤
│                      │                              │        │ Handler     │
│                      │                              │        ├─────────────┤
│                      │                              │        │ Runtime     │
│                      │                              │        ├─────────────┤
│ checker              │ Aliyun::Serverless::Function │ Add    │ Timeout     │
│                      │                              │        ├─────────────┤
│                      │                              │        │ MemorySize  │
│                      │                              │        ├─────────────┤
│                      │                              │        │ CodeUri     │
├──────────────────────┼──────────────────────────────┼────────┼─────────────┤
│                      │                              │        │ Handler     │
│                      │                              │        ├─────────────┤
│                      │                              │        │ Runtime     │
│                      │                              │        ├─────────────┤
│ http-checker         │ Aliyun::Serverless::Function │ Add    │ Timeout     │
│                      │                              │        ├─────────────┤
│                      │                              │        │ MemorySize  │
│                      │                              │        ├─────────────┤
│                      │                              │        │ CodeUri     │
├──────────────────────┼──────────────────────────────┼────────┼─────────────┤
│                      │                              │        │ AuthType    │
│ httpTrigger          │ HTTP                         │ Add    ├─────────────┤
│                      │                              │        │ Methods     │
└──────────────────────┴──────────────────────────────┴────────┴─────────────┘

Waiting for service connectivity-checker to be deployed...
        Waiting for function checker to be deployed...
                Waiting for packaging function checker code...
                The function checker has been packaged. A total of 1 file were compressed and the final size was 1.29 KB
        function checker deploy success
        Waiting for function http-checker to be deployed...
                Waiting for packaging function http-checker code...
                The function http-checker has been packaged. A total of 1 file were compressed and the final size was 1.29 KB
                Waiting for HTTP trigger httpTrigger to be deployed...
                triggerName: httpTrigger
                methods: [ 'GET', 'POST' ]
                url: https://xxx.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/connectivity-checker/http-checker/
                Http Trigger will forcefully add a 'Content-Disposition: attachment' field to the response header, which cannot be overwritten 
                and will cause the response to be downloaded as an attachment in the browser. This issue can be avoided by using CustomDomain.

                trigger httpTrigger deploy success
        function http-checker deploy success
service connectivity-checker deploy success
```
2. Check the connectivity
```
$ echo  '{"host":"baidu.com","port":80,"timeout":5}' | fun invoke connectivity-checker/checker
========= FC invoke Logs begin =========
FC Invoke Start RequestId: eeaeb5b1-a4ac-413a-8ce1-6893d0f2aba8
Socket connect result: 0
Result of checking  baidu.com:80
{
    "TimeTakenInMs": 24,
    "Available": true
}
FC Invoke End RequestId: eeaeb5b1-a4ac-413a-8ce1-6893d0f2aba8

Duration: 26.19 ms, Billed Duration: 100 ms, Memory Size: 128 MB, Max Memory Used: 11.11 MB
========= FC invoke Logs end =========

FC Invoke Result:
{
    "Available": true,
    "TimeTakenInMs": 24
}
```

3. Check the connectivity with the http function. Make sure you replace the http function endpoint with your own.
```
$ curl -d '{"host":"baidu.com","port":8080}' https://xxx.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/connectivity-checker/http-checker/
{
    "TimeTakenInMs": 20012,
    "Available": false
}
```
