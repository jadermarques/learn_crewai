import re
# Copy the guardrail function
### START CODE HERE ###

def write_report_guardrail(output):
    # get the raw output from the TaskOutput object
    try:
        output = output if type(output)==str else output.raw 
    except Exception as e:
        return (False, ("Error retrieving the `raw` argument: "
                        f"\n{str(e)}\n"
                        )
                )
    
    # convert the output to lowecase
    output_lower = output.lower()

    # check that the summary section exists
    if not re.search(r'#+.*summary|#+.*resumo', output_lower):
        return (False, 
                "The report must include a Summary section with a header like '## Summary' or '## Resumo'"
                )

    # check that the insights or recommendations sections exist
    if not re.search(r'#+.*insights|#+.*recommendations|#+.*conclusões|#+.*recomendações', output_lower):
        return (False, 
                "The report must include an Insights section with a header like '## Insights', '## Conclusões' or '## Recomendações'"
                )

    # check that the citations (or references) section exists
    if not re.search(r'#+.*citations|#+.*references|#+.*referências|#+.*bibliografia', output_lower): 
        return (False, 
                "The report must include a Citations (or References) section with a header like '## Citations', '## Referências' or '## Bibliografia'"
                ) 
    return (True, output)

### END CODE HERE ###