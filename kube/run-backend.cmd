@echo off

set KUBECTL=kubectl

echo The location of kubectl is: %KUBECTL%

set KUBECONFIG="%~dp0kubeconfig.yml"

echo kube config file: %KUBECONFIG%

%KUBECTL% apply -f "%~dp0backend-deployment.yml"

for /f "tokens=*" %%i in ( '%KUBECTL% get pods -o=name --selector="app=backend"' ) do (
    echo backend deployment's pod: %%i
    @REM kubectl port-forward %%i 8080:8080 > %~dp0logs/backend-log.txt
)