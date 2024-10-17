import torch.nn as nn
import torch

def loss_func(logits, targets, mask, num_labels, anmerkung=False):
    criterion = nn.CrossEntropyLoss()
    
    if anmerkung:
        active_loss = mask.view(-1) == 1
        active_targets = torch.where(
            active_loss,
            targets.view(-1),
            torch.tensor(criterion.ignore_index).type_as(targets)
        )
        logits = logits.view(-1,num_labels)
        loss = criterion(logits,active_targets)
    else:
        loss = criterion(logits,targets.view(-1))

    return loss

def eval_fn(data_loader, model,device, batch=None):
    model = model.eval()
    final_loss = 0

    with torch.no_grad():
        for bi, batch in enumerate(data_loader):

            for k, v in batch.items():
                batch[k] = v.to(device)

            (
                anmerkung_logits,
                absicht_logits,
                szenario_logits) = model(
                                            batch['ids'], 
                                            batch['mask'],
                                            batch['token_type_ids'])
            
            anmerkung_loss =  loss_func(anmerkung_logits,batch['target_anmerkung'],batch['mask'],model.num_anmerkung, anmerkung=True)
            absicht_loss =  loss_func(absicht_logits,batch['target_absicht'],batch['mask'],model.num_absicht)
            szenario_loss =  loss_func(szenario_logits,batch['target_szenario'],batch['mask'],model.num_szenario)
            
            loss = (anmerkung_loss + absicht_loss + szenario_loss)/3
            final_loss += loss

    return final_loss/len(data_loader)

def train_fn(data_loader,
             model,
             optimizer,
             scheduler,
             device,
             batch = None
            ):

    model = model.train() # model.train()
    final_loss = 0

    for bi, batch in enumerate(data_loader):
        for k,v in batch.items():
            batch[k] = v.to(device)

        # zero the optimizer
        optimizer.zero_grad()

        # Forward pass (output)
        (
            anmerkung_logits,
            absicht_logits,
            szenario_logits) =  model(
                                        batch['ids'], 
                                        batch['mask'],
                                        batch['token_type_ids']
                                    )
        # caculate loss
        anmerkung_loss =  loss_func(anmerkung_logits, batch['target_anmerkung'], batch['mask'], model.num_anmerkung, anmerkung=True)
        absicht_loss =  loss_func(absicht_logits, batch['target_absicht'], batch['mask'], model.num_absicht)
        szenario_loss =  loss_func(szenario_logits, batch['target_szenario'], batch['mask'], model.num_szenario)

        loss = (anmerkung_loss + absicht_loss + szenario_loss)/3

        # Backward pass
        loss.backward()
        
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0) # membatasi norma dari gradien model 
        
        optimizer.step()
        
        scheduler.step()

        final_loss += loss.item()

    return final_loss/len(data_loader)