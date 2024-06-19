@echo off

set KUBECTL=kubectl

echo The location of kubectl is: %KUBECTL%

set KUBECONFIG="%~dp0kubeconfig.yml"

echo kube config file: %KUBECONFIG%

%KUBECTL% apply -f "%~dp0db-deployment.yml"

for /f "tokens=*" %%i in ( '%KUBECTL% get pods -o=name --selector="app=db"' ) do (
    echo database deployment's pod: %%i
    @REM kubectl port-forward %%i 3306:3306 > %~dp0logs/db-log.txt
)