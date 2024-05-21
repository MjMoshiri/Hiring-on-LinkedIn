with open('data.txt', 'r') as infile:
    lines = [line for line in infile if line.strip() and not line.startswith('Page')]

lines.sort(key=lambda line: (' at ' in line.lower() or ' @ ' in line.lower()), reverse=True)


with open('result.md', 'w') as outfile:
    outfile.write('| Name | Title | Company |\n')
    outfile.write('| ---- | ----- | ------- |\n')
    for line in lines:
        name, title_company = line.split(' - ', 1)
        name = name.replace('|', '-') 
        title_company = title_company.replace('|', '-')  
        title_company_lower = title_company.lower()
        if ' at ' in title_company_lower or ' @ ' in title_company_lower:
            split_char = ' at ' if ' at ' in title_company_lower else ' @ '
            parts = title_company.rsplit(split_char, 2)
            title, company = parts[0], parts[1] if len(parts) > 1 else ''
        else:
            title = title_company
            company = ''
        outfile.write(f'| {name} | {title} | {company} |\n')


