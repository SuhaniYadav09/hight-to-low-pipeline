import streamlit as st
import json
import re
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Req2Spec - Business to Technical Converter",
    page_icon="🔧",
    layout="wide"
)

class RequirementAnalyzer:
    def __init__(self):
        self.common_modules = {
            'user management': ['authentication', 'authorization', 'user_profile', 'session_management'],
            'data processing': ['data_validation', 'data_transformation', 'data_storage', 'data_retrieval'],
            'api': ['rest_api', 'request_handler', 'response_formatter', 'error_handler'],
            'database': ['database_connection', 'crud_operations', 'data_models', 'migrations'],
            'frontend': ['user_interface', 'components', 'routing', 'state_management'],
            'notification': ['email_service', 'push_notifications', 'notification_queue', 'templates'],
            'payment': ['payment_gateway', 'transaction_processing', 'billing', 'invoice_generation'],
            'analytics': ['data_collection', 'reporting', 'dashboard', 'metrics_calculation']
        }
        
        self.schema_templates = {
            'user': {
                'id': 'UUID',
                'username': 'String',
                'email': 'String',
                'password_hash': 'String',
                'created_at': 'DateTime',
                'updated_at': 'DateTime',
                'is_active': 'Boolean'
            },
            'product': {
                'id': 'UUID',
                'name': 'String',
                'description': 'Text',
                'price': 'Decimal',
                'category_id': 'UUID',
                'created_at': 'DateTime',
                'is_available': 'Boolean'
            },
            'order': {
                'id': 'UUID',
                'user_id': 'UUID',
                'total_amount': 'Decimal',
                'status': 'Enum',
                'created_at': 'DateTime',
                'updated_at': 'DateTime'
            }
        }

    def extract_entities(self, requirement):
        """Extract key entities from the requirement text"""
        entities = []
        common_entities = ['user', 'product', 'order', 'payment', 'customer', 'admin', 'report', 'notification']
        
        req_lower = requirement.lower()
        for entity in common_entities:
            if entity in req_lower:
                entities.append(entity)
        
        # Extract potential custom entities (nouns that might be important)
        words = re.findall(r'\b[a-zA-Z]+\b', requirement)
        for word in words:
            if word.lower() not in ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among', 'under', 'over']:
                if len(word) > 3 and word.lower() not in entities:
                    entities.append(word.lower())
        
        return list(set(entities))[:8]  # Limit to top 8 entities

    def identify_modules(self, requirement):
        """Identify relevant modules based on requirement keywords"""
        req_lower = requirement.lower()
        identified_modules = []
        
        for module_category, modules in self.common_modules.items():
            if module_category in req_lower or any(keyword in req_lower for keyword in ['login', 'register', 'auth', 'sign'] if module_category == 'user management'):
                identified_modules.extend(modules)
            elif any(keyword in req_lower for keyword in ['store', 'save', 'retrieve', 'process'] if module_category == 'data processing'):
                identified_modules.extend(modules)
            elif any(keyword in req_lower for keyword in ['api', 'endpoint', 'service'] if module_category == 'api'):
                identified_modules.extend(modules)
            elif any(keyword in req_lower for keyword in ['database', 'data', 'store'] if module_category == 'database'):
                identified_modules.extend(modules)
            elif any(keyword in req_lower for keyword in ['interface', 'ui', 'frontend', 'web'] if module_category == 'frontend'):
                identified_modules.extend(modules)
            elif any(keyword in req_lower for keyword in ['notify', 'alert', 'email', 'message'] if module_category == 'notification'):
                identified_modules.extend(modules)
            elif any(keyword in req_lower for keyword in ['payment', 'pay', 'billing', 'charge'] if module_category == 'payment'):
                identified_modules.extend(modules)
            elif any(keyword in req_lower for keyword in ['report', 'analytics', 'dashboard', 'metrics'] if module_category == 'analytics'):
                identified_modules.extend(modules)
        
        return list(set(identified_modules))[:6]  # Limit to top 6 modules

    def generate_schemas(self, entities):
        """Generate database schemas based on identified entities"""
        schemas = {}
        
        for entity in entities:
            if entity in self.schema_templates:
                schemas[entity] = self.schema_templates[entity]
            else:
                # Generate basic schema for custom entities
                schemas[entity] = {
                    'id': 'UUID',
                    'name': 'String',
                    'description': 'Text',
                    'created_at': 'DateTime',
                    'updated_at': 'DateTime',
                    'is_active': 'Boolean'
                }
        
        return schemas

    def generate_pseudocode(self, requirement, modules, entities):
        """Generate pseudocode based on the requirement"""
        pseudocode = []
        
        # Main function
        pseudocode.append("MAIN FUNCTION:")
        pseudocode.append("  BEGIN")
        
        # Add authentication if user management is involved
        if any('auth' in module for module in modules):
            pseudocode.append("    // Authentication")
            pseudocode.append("    IF user_not_authenticated THEN")
            pseudocode.append("      REDIRECT to login_page")
            pseudocode.append("    END IF")
            pseudocode.append("")
        
        # Add data processing logic
        if any('data' in module for module in modules):
            pseudocode.append("    // Data Processing")
            pseudocode.append("    INPUT user_data")
            pseudocode.append("    VALIDATE user_data")
            pseudocode.append("    IF validation_fails THEN")
            pseudocode.append("      RETURN error_message")
            pseudocode.append("    END IF")
            pseudocode.append("")
        
        # Add main business logic
        pseudocode.append("    // Main Business Logic")
        for entity in entities[:3]:  # Process top 3 entities
            pseudocode.append(f"    PROCESS {entity}_operations")
            pseudocode.append(f"    STORE {entity}_data IN database")
        
        pseudocode.append("")
        
        # Add notification logic if needed
        if any('notification' in module for module in modules):
            pseudocode.append("    // Notifications")
            pseudocode.append("    SEND notification_to_user")
            pseudocode.append("    LOG notification_sent")
            pseudocode.append("")
        
        # Add API response
        if any('api' in module for module in modules):
            pseudocode.append("    // API Response")
            pseudocode.append("    RETURN success_response WITH data")
        
        pseudocode.append("  END")
        
        return "\n".join(pseudocode)

    def analyze_requirement(self, requirement):
        """Main method to analyze requirement and generate technical specs"""
        entities = self.extract_entities(requirement)
        modules = self.identify_modules(requirement)
        schemas = self.generate_schemas(entities)
        pseudocode = self.generate_pseudocode(requirement, modules, entities)
        
        return {
            'entities': entities,
            'modules': modules,
            'schemas': schemas,
            'pseudocode': pseudocode,
            'timestamp': datetime.now().isoformat()
        }

# Initialize the analyzer
@st.cache_resource
def get_analyzer():
    return RequirementAnalyzer()

analyzer = get_analyzer()

# Streamlit UI
st.title("🔧 Req2Spec - Business to Technical Converter")
st.markdown("Convert high-level business requirements into detailed technical specifications automatically!")

# Sidebar with examples
st.sidebar.header("📋 Example Requirements")
examples = [
    "Create a user registration system with email verification",
    "Build an e-commerce platform with product catalog and payment processing",
    "Develop a task management system with notifications and reporting",
    "Create a blog platform with user authentication and comment system"
]

selected_example = st.sidebar.selectbox("Choose an example:", [""] + examples)

# Main input area
st.header("📝 Input Business Requirement")
requirement_text = st.text_area(
    "Enter your high-level business requirement:",
    value=selected_example if selected_example else "",
    height=150,
    placeholder="e.g., Create a user management system that allows registration, login, and profile management with email notifications..."
)

# Analysis button
if st.button("🚀 Generate Technical Specifications", type="primary"):
    if requirement_text.strip():
        with st.spinner("Analyzing requirement and generating specifications..."):
            result = analyzer.analyze_requirement(requirement_text)
        
        # Display results
        st.success("✅ Analysis Complete!")
        
        # Create tabs for different outputs
        tab1, tab2, tab3, tab4 = st.tabs(["📦 Modules", "🗄️ Database Schemas", "💻 Pseudocode", "📄 JSON Export"])
        
        with tab1:
            st.header("Identified Modules")
            if result['modules']:
                cols = st.columns(2)
                for i, module in enumerate(result['modules']):
                    with cols[i % 2]:
                        st.code(module, language="text")
            else:
                st.info("No specific modules identified. Consider adding more details to your requirement.")
        
        with tab2:
            st.header("Database Schemas")
            if result['schemas']:
                for entity, schema in result['schemas'].items():
                    st.subheader(f"{entity.title()} Schema")
                    schema_code = f"CREATE TABLE {entity} (\n"
                    for field, data_type in schema.items():
                        schema_code += f"  {field} {data_type},\n"
                    schema_code = schema_code.rstrip(',\n') + "\n);"
                    st.code(schema_code, language="sql")
            else:
                st.info("No entities identified for schema generation.")
        
        with tab3:
            st.header("Generated Pseudocode")
            st.code(result['pseudocode'], language="text")
        
        with tab4:
            st.header("Complete Specification (JSON)")
            st.json(result)
            
            # Download button
            json_str = json.dumps(result, indent=2)
            st.download_button(
                label="📥 Download as JSON",
                data=json_str,
                file_name=f"technical_spec_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    else:
        st.error("Please enter a business requirement to analyze.")

# Footer
st.markdown("---")
st.markdown("**How to use:** Enter your business requirement in plain English, and the tool will automatically break it down into modules, database schemas, and pseudocode.")

# Instructions for deployment
with st.expander("🚀 Deployment Instructions"):
    st.markdown("""
    **Deploy to Streamlit Cloud:**
    1. Create a new repository on GitHub
    2. Add this code as `app.py`
    3. Create `requirements.txt` with: `streamlit`
    4. Go to [share.streamlit.io](https://share.streamlit.io)
    5. Connect your GitHub repo and deploy!
    
    **Local Development:**
    ```bash
    pip install streamlit
    streamlit run app.py
    ```
    """)
