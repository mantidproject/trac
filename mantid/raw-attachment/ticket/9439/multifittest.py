
# create a workspace with 3 spectra and a single point in each. x-values of each spctrum are different.
ws = CreateWorkspace([1,2,3], [0,0,0],[1,1,1],3)

# define a multi-domain function with a single member which is to be applied to 3 domains with indices form 0 to 2.
fun = 'composite=MultiDomainFunction;name=UserFunction,Formula="x",$domains=(0-2)'

# specify additional spectra using properties InputWorkspace_# and WorkspaceIndex_#
kwargs = {
        'MaxIterations':0,
        'CreateOutput':1,
        'InputWorkspace_1': ws,
        'WorkspaceIndex_1': 1,    # domain 1
        'InputWorkspace_2': ws,
        'WorkspaceIndex_2': 2,    # domain 2
        }

# evaluate the function
Fit(fun,ws,**kwargs)

# check the output ws_Workspaces: Calc-values should be equal to x-values
