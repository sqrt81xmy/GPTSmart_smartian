// ------------------------------------------------------------------------------
// <auto-generated>
//    Generated by avrogen, version 1.7.7.5
//    Changes to this file may cause incorrect behavior and will be lost if code
//    is regenerated
// </auto-generated>
// ------------------------------------------------------------------------------

using System.Collections.Generic;
using Avro;
using Avro.Specific;

namespace Nethermind.PubSub.Kafka.Consumer.Avro.Models
{
	public partial class Log : ISpecificRecord
	{
		public static Schema _SCHEMA = Schema.Parse(@"{""type"":""record"",""name"":""Log"",""namespace"":""Nethermind.PubSub.Kafka.Avro.Models"",""fields"":[{""name"":""address"",""type"":""string""},{""name"":""logTopics"",""type"":{""type"":""array"",""items"":""string""}},{""name"":""data"",""type"":""string""},{""name"":""blockNumber"",""type"":""long""},{""name"":""transactionHash"",""type"":""string""},{""name"":""transactionIndex"",""type"":""int""},{""name"":""blockHash"",""type"":""string""},{""name"":""logIndex"",""type"":""int""},{""name"":""removed"",""type"":""boolean""}]}");
		private string _address;
		private IList<System.String> _logTopics;
		private string _data;
		private long _blockNumber;
		private string _transactionHash;
		private int _transactionIndex;
		private string _blockHash;
		private int _logIndex;
		private bool _removed;
		public virtual Schema Schema
		{
			get
			{
				return Log._SCHEMA;
			}
		}
		public string address
		{
			get
			{
				return this._address;
			}
			set
			{
				this._address = value;
			}
		}
		public IList<System.String> logTopics
		{
			get
			{
				return this._logTopics;
			}
			set
			{
				this._logTopics = value;
			}
		}
		public string data
		{
			get
			{
				return this._data;
			}
			set
			{
				this._data = value;
			}
		}
		public long blockNumber
		{
			get
			{
				return this._blockNumber;
			}
			set
			{
				this._blockNumber = value;
			}
		}
		public string transactionHash
		{
			get
			{
				return this._transactionHash;
			}
			set
			{
				this._transactionHash = value;
			}
		}
		public int transactionIndex
		{
			get
			{
				return this._transactionIndex;
			}
			set
			{
				this._transactionIndex = value;
			}
		}
		public string blockHash
		{
			get
			{
				return this._blockHash;
			}
			set
			{
				this._blockHash = value;
			}
		}
		public int logIndex
		{
			get
			{
				return this._logIndex;
			}
			set
			{
				this._logIndex = value;
			}
		}
		public bool removed
		{
			get
			{
				return this._removed;
			}
			set
			{
				this._removed = value;
			}
		}
		public virtual object Get(int fieldPos)
		{
			switch (fieldPos)
			{
			case 0: return this.address;
			case 1: return this.logTopics;
			case 2: return this.data;
			case 3: return this.blockNumber;
			case 4: return this.transactionHash;
			case 5: return this.transactionIndex;
			case 6: return this.blockHash;
			case 7: return this.logIndex;
			case 8: return this.removed;
			default: throw new AvroRuntimeException("Bad index " + fieldPos + " in Get()");
			};
		}
		public virtual void Put(int fieldPos, object fieldValue)
		{
			switch (fieldPos)
			{
			case 0: this.address = (System.String)fieldValue; break;
			case 1: this.logTopics = (IList<System.String>)fieldValue; break;
			case 2: this.data = (System.String)fieldValue; break;
			case 3: this.blockNumber = (System.Int64)fieldValue; break;
			case 4: this.transactionHash = (System.String)fieldValue; break;
			case 5: this.transactionIndex = (System.Int32)fieldValue; break;
			case 6: this.blockHash = (System.String)fieldValue; break;
			case 7: this.logIndex = (System.Int32)fieldValue; break;
			case 8: this.removed = (System.Boolean)fieldValue; break;
			default: throw new AvroRuntimeException("Bad index " + fieldPos + " in Put()");
			};
		}
	}
}
