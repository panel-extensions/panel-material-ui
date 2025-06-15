import pandas as pd

def generate_company_html(row: pd.Series, image_width: str='40px'):
    company_name=row["Company"]
    company_image_url=row["CompanyImage"]
    html = f'''
    <div style="display: flex; align-items: center; gap: 10px;">
        <img src="{company_image_url}" alt="{company_name}" style="width: {image_width}; height: auto;">
        <h4>{company_name}</h4>
    </div>
    '''
    return html

def generate_progress_bar(row: pd.Series):
    completion_percent = int(round(float(row["Completion"]),0))
    color = 'green' if completion_percent >=99.999 else 'blue'
    html = f'''
    <div style=\"width: 100%;\">
        <div style=\"margin-bottom: 4px; font-size: 12px; text-align: left;\">{completion_percent}%</div>
        <div style=\"width: 100%; background-color: #e0e0e0; border-radius: 4px; overflow: hidden; height: 5px;\">
            <div style=\"width: {completion_percent}%; background-color: {color}; height: 100%;\"></div>
        </div>
    </div>
    '''
    return html

def generate_member_images(row: pd.Series, image_size: str='30px', overlap_offset: str='-10px'):
    members = row["Members"]
    images_html = ''
    for idx, member in enumerate(members):
        images_html += f'''
        <img src=\"{member['Image']}\" title=\"{member['Name']}\"
             style=\"
                width: {image_size};
                height: {image_size};
                border-radius: 50%;
                border: 2px solid white;
                position: relative;
                left: {idx * int(overlap_offset.replace('px', ''))}px;
                z-index: {len(members)-idx};
                transition: transform 0.2s;
             \"
             onmouseover=\"this.style.transform='scale(1.2)';this.style.zIndex='{len(members)+1}'\"
             onmouseout=\"this.style.transform='scale(1)';this.style.zIndex='{len(members)-idx}'\"
        >
        '''
    wrapper_html = f'''
    <div style=\"display: flex; align-items: center;\">
        {images_html}
    </div>
    '''
    return wrapper_html

def render_author(row: pd.Series):
    return (
        f'<div style="display:flex; align-items:center; gap:10px;">'
        f'<img src="{row["image"]}" alt="img" style="width:35px; height:35px; border-radius:50%; object-fit:cover;">'
        f'<div><div style="font-weight:600;">{row["name"]}</div><div style="font-size:12px;color:gray;">{row["email"]}</div></div>'
        f"</div>"
    )

def render_function(row: pd.Series):
    return f'<div><div style="font-weight:600;">{row["title"]}</div><div style="font-size:12px;color:gray;">{row["team"]}</div></div>'

def render_status(row: pd.Series):
    color = "#43a047" if row["status"] == "Online" else "#747b8a"

    return f'<span style="background-color:{color}; color:white; padding:3px 8px; border-radius:5px; font-size:12px;">{row["status"]}</span>'

def render_edit_button():
    return '<button style="color:black;border:none;padding:6px 12px;border-radius:4px;cursor:pointer;">Edit</button>'
