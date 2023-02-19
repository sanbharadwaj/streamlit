import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title='FFS Logs',  layout='wide', page_icon=':ambulance:')


# Ask the user to upload a JSON file
uploaded_file = st.file_uploader('Upload a JSON file', type='json')

# If a file was uploaded, read its contents as a JSON object
if uploaded_file is not None:
    try:
        file_contents = uploaded_file.read().decode('utf-8')
        json_data = json.loads(file_contents)
        

        dfo = pd.json_normalize(json_data['searchCriteriaResponses'][0]['scheduleCriteriaResponse'][0]['originDestinations'][0]['segments'])
        dfo['originIndex'] = 0
        dfo.set_index("originIndex", inplace=True)

        for i in range(1, len(json_data['searchCriteriaResponses'][0]['scheduleCriteriaResponse'][0]['originDestinations'])):
            dfi = pd.json_normalize(json_data['searchCriteriaResponses'][0]['scheduleCriteriaResponse'][0]['originDestinations'][i]['segments'])
            dfi['originIndex'] = i
            dfi.set_index("originIndex", inplace=True)
            dfo = pd.concat([dfo,dfi])

        # Create prompt asking user to enter airline code
        airline_code_1 = st.text_input('Enter the airline code for outbound')
        st.dataframe(dfo[dfo['carrierCode'] == airline_code_1])

        dfr = pd.json_normalize(json_data['searchCriteriaResponses'][0]['scheduleCriteriaResponse'][1]['originDestinations'][0]['segments'])
        dfr['destinationIndex'] = 0
        dfr.set_index("destinationIndex", inplace=True)

        for i in range(1, len(json_data['searchCriteriaResponses'][0]['scheduleCriteriaResponse'][1]['originDestinations'])):
            dfi = pd.json_normalize(json_data['searchCriteriaResponses'][0]['scheduleCriteriaResponse'][1]['originDestinations'][i]['segments'])
            dfi['destinationIndex'] = i
            dfi.set_index("destinationIndex", inplace=True)
            dfr = pd.concat([dfr,dfi])
        
        # Create prompt asking user to enter airline code
        airline_code_2 = st.text_input('Enter the airline code for inbound')
        st.dataframe(dfr[dfr['carrierCode'] == airline_code_2])
        
        # Ask user for origin index number -- data type is int
        originIndex = st.number_input('Enter the Origin index number', min_value=0, max_value=100000, step=1)

        
        # Ask user for destination index number
        destinationIndex = st.number_input('Enter the Destination index number', min_value=0, max_value=100000, step=1)
        
        product_list = []

        for i in range(0, len(json_data['searchCriteriaResponses'][0]['products'])):
            if json_data['searchCriteriaResponses'][0]['products'][i]['itineraryReferences'][0]['originDestinationResponseIndex'] == originIndex and json_data['searchCriteriaResponses'][0]['products'][i]['itineraryReferences'][1]['originDestinationResponseIndex'] == destinationIndex:
                product_list.append(i)
                st.write(f'Product Number is {i}')



        
        # Ask user for product number
        product_number = st.number_input('Enter the product number', min_value=0, max_value=100000, step=1)

        st.write(f"Provider is {json_data['searchCriteriaResponses'][0]['products'][product_number]['providerContext']['providerCode']}")

        for item in json_data['searchCriteriaResponses'][0]['products'][product_number]['fareList'][0].keys():
            if type(json_data['searchCriteriaResponses'][0]['products'][product_number]['fareList'][0][item]) is not str:
                df22 = pd.json_normalize(json_data['searchCriteriaResponses'][0]['products'][product_number]['fareList'][0][item])
                st.dataframe(df22)

        # for item in json_data['searchCriteriaResponses'][0]['products'][product_number]['fareTotal'][0].keys():
        #     if type(json_data['searchCriteriaResponses'][0]['products'][product_number]['fareTotal'][0][item]) is not str:
        #         df23 = pd.json_normalize(json_data['searchCriteriaResponses'][0]['products'][product_number]['fareTotal'][0][item])
        #         st.write(df23)

        df20a = json.dumps(json_data['searchCriteriaResponses'][0]['products'][141])
        st.write(json.loads(df20a))

    except json.JSONDecodeError as e:
        st.write('Error decoding JSON:', e)

