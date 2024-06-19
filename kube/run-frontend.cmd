@echo off

set KUBECTL=kubectl

echo The location of kubectl is: %KUBECTL%

set KUBECONFIG="%~dp0kubeconfig.yml"

echo kube config file: %KUBECONFIG%

%KUBECTL% apply -f "%~dp0frontend-deployment.yml"

for /f "tokens=*" %%i in ( '%KUBECTL% get pods -o=name --selector="app=frontend"' ) do (
    echo frontend deployment's pod: %%i
    @REM kubectl port-forward %%i 80:80 > %~dp0logs/frontend-log.txt
)