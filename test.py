import logging
from signalwire.relay.consumer import Consumer

class CustomConsumer(Consumer):
  def setup(self):
    self.project = 'b24d407b-27fd-44ee-b541-979948bb61b8'
    self.token = 'PT7a41d172eb00d6d7194d16a67076c4cd498c594a402e3552PT2c6c54ce037d7301a3226c6cefdea5335e2f3296f0641e94'
    self.contexts = ['office']

  async def ready(self):
    logging.info('CustomConsumer is ready!')
    # Replace numbers with yours!
    result = await self.client.messaging.send(context='office', to_number='+13177213016', from_number='+14195586216', body='Welcome to SignalWire!')
    if result.successful:
      logging.info(f'Message sent. ID: {result.message_id}')

consumer = CustomConsumer()
consumer.run()