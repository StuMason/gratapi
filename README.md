# GratApi

Gratitude journal. Saved in daily logs. Cognito secured.

## Overview

Uses console built cognito user pool for authentication.

Writes gratitudes to daily journal against authenticated users email.

## Adding environment variables

1. add the parameter to the .env file, this is not in the git repo, so you're safe (add to example.env too) `FOO=secret123`
2. add the parameter TWICE in the template.yaml - once in Parameters and once in Globals > Variables (using a ref)
3. add the .env paramter to the --parameter-overrides in the `deploy` section of the makefile.

The above means you need to make 4-5 changes to add a single environment param to the deploy.

Also means you can't have staging/production unless you had a different script for each one? That's do able.
