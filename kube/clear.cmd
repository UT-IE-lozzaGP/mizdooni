@echo off

set KUBECTL=kubectl

echo The location of kubectl is: %KUBECTL%

set KUBECONFIG="%~dp0kubeconfig.yml"

%KUBECTL% delete pods --all
%KUBECTL% delete services --all
%KUBECTL% delete deployments --all
%KUBECTL% delete pvc --all
%KUBECTL% delete po --all