from google.cloud import talent_v4beta1
import six

def sample_list_jobs(project_id, filter_=r'companyName="Amazon"'):
    """List Jobs"""
    client = talent_v4beta1.JobServiceClient.from_service_account_file("job-search-api-dli-1e09541fd828.json")
    # client = talent_v4beta1.gapic.profile_service_client.from_service_account_file()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # filter_ = 'companyName=projects/my-project/companies/company-id'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode('utf-8')
    if isinstance(filter_, six.binary_type):
        filter_ = filter_.decode('utf-8')
    parent = client.project_path(project_id)
    # tenant = client.create_tenant
    # Iterate over all results
    for response_item in client.list_jobs(parent, filter_):
        print('Job name: {}'.format(response_item.name))
        print('Job requisition ID: {}'.format(response_item.requisition_id))
        print('Job title: {}'.format(response_item.title))
        print('Job description: {}'.format(response_item.description))

sample_list_jobs('job-search-api-dli')