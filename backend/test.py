def create_work_email(first_name:str, last_name:str):
    
    company_domain="@homesync.com"
    
    return f"{first_name}.{last_name}{company_domain}"

print(create_work_email("pranavkumaran","balamurugan"))