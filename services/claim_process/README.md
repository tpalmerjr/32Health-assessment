# Claims Service

## Top 10 Provider NPIs
To obtain the top 10 provider NPIs, I created a service that the 
"/top-providers/" endpoint calls. The service uses a utility method for the
computation. The method assumes that the net_fee value has not been stored in the 
database. I did this to show how this could work with an algorithm. It is possible 
to get the distinct NPIs from the database with a query.

The algorithm pulls all claim information from the database. It then loops through
each claim and computes the net_fee. It adds this value to a dictionary based on
the NPI. Because the directions stated net_fees (plural) generated, this value for the 
NPI is cumulative. It then iterates over the dictionary and adds the npi and net_fee to
heapq (priority-queue). It pops (smallest) one off if the length is greater than 10. It
then extracts the 10 NPIs into a list and returns them.

## Claim Process Service and Payment Service Communication
Assuming that multiple instances of both services will be running and that there will be
running and that we would not want to hold up the claims service to wait for a response
from the payments service, I would implement a messaging system for communication purposes.
This could include the use of SQS, Redis, RabbitMQ, Kafka, or another similar systems. This
would include a stream for communication from the Claims Process Service to the Payments
Service. The Payments Service would pull from the que and process payments for the claim.
In the case where a payment could not be processed, there would be a que for the Payments
Service to add a payload to indicating there is an issue in processing the payment for a
claim. There will be a claims process service that will pull from this que and handle the
failed payments. Having the two ques will allow services to complete without waiting on
downstream services. It will allow for the Claim Creation Process, Payment Process, and
potentially a ClaimPaymentFailure Process to be scaled individually. It is possible that
there may need to be more Claim Process and Payment Process services running versus the
amount of ClaimPaymentFailure Processes services running. Being able to horizontally scale
these services individual allows for more efficient resource utilization as well as it is
more cost-effective.
